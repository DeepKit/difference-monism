from collections import defaultdict, OrderedDict


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq = {}  # key -> [value, frequency]
        self.freq_to_keys = defaultdict(OrderedDict)  # frequency -> OrderedDict of keys
    
    def _update_freq(self, key: int) -> None:
        value, freq = self.key_to_val_freq[key]
        
        # Remove key from current frequency bucket
        del self.freq_to_keys[freq][key]
        
        # Update min_freq if current bucket is empty
        if not self.freq_to_keys[freq] and freq == self.min_freq:
            self.min_freq += 1
        
        # Add key to new frequency bucket
        new_freq = freq + 1
        self.freq_to_keys[new_freq][key] = None
        self.key_to_val_freq[key] = [value, new_freq]
    
    def get(self, key: int) -> int:
        if key not in self.key_to_val_freq:
            return -1
        
        self._update_freq(key)
        return self.key_to_val_freq[key][0]
    
    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        
        # Update existing key
        if key in self.key_to_val_freq:
            self.key_to_val_freq[key][0] = value
            self._update_freq(key)
            return
        
        # Evict if at capacity
        if len(self.key_to_val_freq) >= self.capacity:
            # Remove least frequently used (and least recently used if tie)
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val_freq[evict_key]
        
        # Add new key
        self.key_to_val_freq[key] = [value, 1]
        self.freq_to_keys[1][key] = None
        self.min_freq = 1


# 使用示例
if __name__ == "__main__":
    cache = LFUCache(2)
    
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))       # 返回 1
    cache.put(3, 3)            # 驱逐 key 2
    print(cache.get(2))       # 返回 -1 (未找到)
    print(cache.get(3))       # 返回 3
    cache.put(4, 4)            # 驱逐 key 1
    print(cache.get(1))       # 返回 -1 (未找到)
    print(cache.get(3))       # 返回 3
    print(cache.get(4))       # 返回 4