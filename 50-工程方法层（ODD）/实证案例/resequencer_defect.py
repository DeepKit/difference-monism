class Reorder:
    def __init__(self, items=None):
        self.items = items if items is not None else []
    
    def sort_ascending(self):
        self.items.sort()
        return self
    
    def sort_descending(self):
        self.items.sort(reverse=True)
        return self
    
    def reverse(self):
        self.items.reverse()
        return self
    
    def custom_order(self, key_func):
        self.items.sort(key=key_func)
        return self
    
    def move_to_front(self, index):
        if 0 <= index < len(self.items):
            item = self.items.pop(index)
            self.items.insert(0, item)
        return self
    
    def move_to_back(self, index):
        if 0 <= index < len(self.items):
            item = self.items.pop(index)
            self.items.append(item)
        return self
    
    def swap(self, i, j):
        if 0 <= i < len(self.items) and 0 <= j < len(self.items):
            self.items[i], self.items[j] = self.items[j], self.items[i]
        return self
    
    def shuffle(self):
        import random
        random.shuffle(self.items)
        return self
    
    def get_items(self):
        return self.items
    
    def __repr__(self):
        return f"Reorder({self.items})"


# 使用示例
if __name__ == "__main__":
    # 基本排序
    r = Reorder([3, 1, 4, 1, 5, 9, 2, 6])
    print(r.sort_ascending().get_items())  # [1, 1, 2, 3, 4, 5, 6, 9]
    
    # 降序
    r = Reorder([3, 1, 4, 1, 5])
    print(r.sort_descending().get_items())  # [5, 4, 3, 1, 1]
    
    # 自定义排序
    r = Reorder(['apple', 'pie', 'a', 'longer'])
    print(r.custom_order(len).get_items())  # ['a', 'pie', 'apple', 'longer']
    
    # 移动元素
    r = Reorder([1, 2, 3, 4, 5])
    print(r.move_to_front(3).get_items())  # [4, 1, 2, 3, 5]
    
    # 交换
    r = Reorder([1, 2, 3, 4, 5])
    print(r.swap(0, 4).get_items())  # [5, 2, 3, 4, 1]