import time
import threading


class TokenBucketLimiter:
    def __init__(self, capacity: float, refill_rate: float):
        """
        Token bucket rate limiter.
        
        Args:
            capacity: Maximum number of tokens in the bucket
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
    
    def consume(self, tokens: float = 1) -> bool:
        """
        Try to consume tokens.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were consumed, False otherwise
        """
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_and_consume(self, tokens: float = 1, timeout: float = None) -> bool:
        """
        Wait until tokens are available and consume them.
        
        Args:
            tokens: Number of tokens to consume
            timeout: Maximum wait time in seconds
            
        Returns:
            True if tokens were consumed, False if timeout
        """
        start = time.time()
        while True:
            if self.consume(tokens):
                return True
            
            if timeout and (time.time() - start) >= timeout:
                return False
            
            with self.lock:
                self._refill()
                wait_time = (tokens - self.tokens) / self.refill_rate
            
            time.sleep(min(0.01, wait_time))


# 使用示例
if __name__ == "__main__":
    # 每秒10个请求，桶容量20
    limiter = TokenBucketLimiter(capacity=20, refill_rate=10)
    
    # 快速发送请求
    for i in range(25):
        if limiter.consume():
            print(f"请求 {i+1}: 通过")
        else:
            print(f"请求 {i+1}: 被限流")