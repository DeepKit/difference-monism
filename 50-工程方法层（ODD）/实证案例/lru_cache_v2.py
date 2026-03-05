class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)  # dummy head
        self.tail = Node(0, 0)  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        """Remove node from linked list"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_head(self, node):
        """Add node right after head (most recently used position)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _move_to_head(self, node):
        """Move existing node to head"""
        self._remove(node)
        self._add_to_head(node)
    
    def _pop_tail(self):
        """Remove and return least recently used node"""
        lru_node = self.tail.prev
        self._remove(lru_node)
        return lru_node
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)
        return node.value
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            if len(self.cache) > self.capacity:
                lru_node = self._pop_tail()
                del self.cache[lru_node.key]


# Usage example
if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))    # returns 1
    cache.put(3, 3)        # evicts key 2
    print(cache.get(2))    # returns -1 (not found)
    cache.put(4, 4)        # evicts key 1
    print(cache.get(1))    # returns -1 (not found)
    print(cache.get(3))    # returns 3
    print(cache.get(4))    # returns 4