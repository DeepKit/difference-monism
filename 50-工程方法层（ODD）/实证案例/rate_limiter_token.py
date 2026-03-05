import threading
import time
from typing import Optional


class TokenBucketLimiter:
    def __init__(self, capacity: float, refill_rate: float):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        
        self._capacity = float(capacity)
        self._refill_rate = float(refill_rate)
        self._tokens = float(capacity)
        self._last_refill_time = time.time()
        self._lock = threading.Lock()
    
    def _refill(self) -> None:
        current_time = time.time()
        elapsed = current_time - self._last_refill_time
        tokens_to_add = elapsed * self._refill_rate
        
        self._tokens = min(self._capacity, self._tokens + tokens_to_add)
        self._last_refill_time = current_time
    
    def consume(self, tokens: float = 1.0) -> bool:
        if tokens <= 0:
            raise ValueError("Tokens to consume must be positive")
        if tokens > self._capacity:
            raise ValueError("Tokens requested exceeds bucket capacity")
        
        with self._lock:
            self._refill()
            
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
    
    def try_consume(self, tokens: float = 1.0, timeout: Optional[float] = None) -> bool:
        if tokens <= 0:
            raise ValueError("Tokens to consume must be positive")
        if tokens > self._capacity:
            raise ValueError("Tokens requested exceeds bucket capacity")
        
        start_time = time.time()
        
        while True:
            with self._lock:
                self._refill()
                
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return True
                
                if timeout is not None:
                    elapsed = time.time() - start_time
                    if elapsed >= timeout:
                        return False
                    
                    tokens_needed = tokens - self._tokens
                    wait_time = tokens_needed / self._refill_rate
                    remaining_timeout = timeout - elapsed
                    
                    if wait_time > remaining_timeout:
                        return False
            
            if timeout is None:
                tokens_needed = tokens - self._tokens
                wait_time = tokens_needed / self._refill_rate
            else:
                elapsed = time.time() - start_time
                tokens_needed = tokens - self._tokens
                wait_time = min(tokens_needed / self._refill_rate, timeout - elapsed)
            
            if wait_time > 0:
                time.sleep(wait_time)
    
    def available_tokens(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens
    
    def reset(self) -> None:
        with self._lock:
            self._tokens = self._capacity
            self._last_refill_time = time.time()
    
    @property
    def capacity(self) -> float:
        return self._capacity
    
    @property
    def refill_rate(self) -> float:
        return self._refill_rate