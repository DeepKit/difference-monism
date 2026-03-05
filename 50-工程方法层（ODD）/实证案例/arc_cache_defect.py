from collections import OrderedDict
from typing import Any, Optional


class ARCCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.capacity = capacity
        self.p = 0  # Target size for T1
        
        # T1: Recent cache entries (recency)
        self.t1 = OrderedDict()
        # T2: Frequent cache entries (frequency)
        self.t2 = OrderedDict()
        # B1: Ghost entries for T1
        self.b1 = OrderedDict()
        # B2: Ghost entries for T2
        self.b2 = OrderedDict()
    
    def __len__(self) -> int:
        return len(self.t1) + len(self.t2)
    
    def __contains__(self, key: Any) -> bool:
        return key in self.t1 or key in self.t2
    
    def get(self, key: Any) -> Optional[Any]:
        if key in self.t1:
            value = self.t1.pop(key)
            self.t2[key] = value
            return value
        
        if key in self.t2:
            self.t2.move_to_end(key)
            return self.t2[key]
        
        return None
    
    def put(self, key: Any, value: Any) -> None:
        # Case 1: Key in T1 or T2 (cache hit)
        if key in self.t1:
            self.t1.pop(key)
            self.t2[key] = value
            return
        
        if key in self.t2:
            self.t2[key] = value
            self.t2.move_to_end(key)
            return
        
        # Case 2: Key in B1 (ghost hit in recent)
        if key in self.b1:
            delta = 1 if len(self.b1) >= len(self.b2) else len(self.b2) // len(self.b1)
            self.p = min(self.p + delta, self.capacity)
            self._replace(key, in_b2=False)
            self.b1.pop(key)
            self.t2[key] = value
            return
        
        # Case 3: Key in B2 (ghost hit in frequent)
        if key in self.b2:
            delta = 1 if len(self.b2) >= len(self.b1) else len(self.b1) // len(self.b2)
            self.p = max(self.p - delta, 0)
            self._replace(key, in_b2=True)
            self.b2.pop(key)
            self.t2[key] = value
            return
        
        # Case 4: Cache miss
        l1_size = len(self.t1) + len(self.b1)
        
        if l1_size == self.capacity:
            if len(self.t1) < self.capacity:
                self.b1.popitem(last=False)
                self._replace(key, in_b2=False)
            else:
                evicted_key = self.t1.popitem(last=False)[0]
        
        elif l1_size < self.capacity:
            total_size = len(self.t1) + len(self.t2) + len(self.b1) + len(self.b2)
            if total_size >= self.capacity:
                if total_size == 2 * self.capacity:
                    self.b2.popitem(last=False)
                self._replace(key, in_b2=False)
        
        self.t1[key] = value
    
    def _replace(self, key: Any, in_b2: bool) -> None:
        if len(self.t1) > 0 and (
            (len(self.t1) > self.p) or 
            (key in self.b2 and len(self.t1) == self.p)
        ):
            old_key, old_value = self.t1.popitem(last=False)
            self.b1[old_key] = None
        else:
            if len(self.t2) > 0:
                old_key, old_value = self.t2.popitem(last=False)
                self.b2[old_key] = None
    
    def clear(self) -> None:
        self.t1.clear()
        self.t2.clear()
        self.b1.clear()
        self.b2.clear()
        self.p = 0
    
    def __repr__(self) -> str:
        return (f"ARCCache(capacity={self.capacity}, size={len(self)}, "
                f"p={self.p}, T1={len(self.t1)}, T2={len(self.t2)}, "
                f"B1={len(self.b1)}, B2={len(self.b2)})")


# 使用示例
if __name__ == "__main__":
    cache = ARCCache(capacity=3)
    
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    
    print(cache.get("a"))  # 1
    print(cache.get("b"))  # 2
    
    cache.put("d", 4)  # 驱逐 "c"
    
    print(cache.get("c"))  # None
    print(cache.get("d"))  # 4
    
    print(cache)