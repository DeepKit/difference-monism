import hashlib
from typing import Any


class BloomFilter:
    def __init__(self, size: int = 10000, hash_count: int = 3):
        """
        初始化布隆过滤器
        :param size: 位数组大小
        :param hash_count: 哈希函数数量
        """
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size
    
    def _hash(self, item: Any, seed: int) -> int:
        """生成哈希值"""
        h = hashlib.md5((str(item) + str(seed)).encode('utf-8'))
        return int(h.hexdigest(), 16) % self.size
    
    def add(self, item: Any) -> None:
        """添加元素"""
        for i in range(self.hash_count):
            index = self._hash(item, i)
            self.bit_array[index] = 1
    
    def contains(self, item: Any) -> bool:
        """检查元素是否可能存在"""
        for i in range(self.hash_count):
            index = self._hash(item, i)
            if self.bit_array[index] == 0:
                return False
        return True
    
    def __contains__(self, item: Any) -> bool:
        """支持 in 操作符"""
        return self.contains(item)


# 使用示例
if __name__ == "__main__":
    bf = BloomFilter(size=10000, hash_count=5)
    
    # 添加元素
    bf.add("apple")
    bf.add("banana")
    bf.add("orange")
    
    # 检查元素
    print("apple" in bf)      # True
    print("banana" in bf)     # True
    print("grape" in bf)      # False (可能误判为True)
    print(bf.contains("orange"))  # True