class CircularBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0
    
    def write(self, item):
        """写入数据，如果缓冲区满则覆盖最旧的数据"""
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        
        if self.size < self.capacity:
            self.size += 1
        else:
            self.head = (self.head + 1) % self.capacity
    
    def read(self):
        """读取并移除最旧的数据"""
        if self.is_empty():
            raise IndexError("Buffer is empty")
        
        item = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return item
    
    def peek(self):
        """查看最旧的数据但不移除"""
        if self.is_empty():
            raise IndexError("Buffer is empty")
        return self.buffer[self.head]
    
    def is_empty(self):
        return self.size == 0
    
    def is_full(self):
        return self.size == self.capacity
    
    def __len__(self):
        return self.size
    
    def clear(self):
        """清空缓冲区"""
        self.buffer = [None] * self.capacity
        self.head = 0
        self.tail = 0
        self.size = 0
    
    def __repr__(self):
        items = []
        index = self.head
        for _ in range(self.size):
            items.append(self.buffer[index])
            index = (index + 1) % self.capacity
        return f"CircularBuffer({items})"


# 使用示例
if __name__ == "__main__":
    cb = CircularBuffer(5)
    
    # 写入数据
    for i in range(7):
        cb.write(i)
        print(f"写入 {i}: {cb}")
    
    # 读取数据
    print(f"\n读取: {cb.read()}")
    print(f"当前状态: {cb}")
    
    # 查看数据
    print(f"查看: {cb.peek()}")
    print(f"大小: {len(cb)}")