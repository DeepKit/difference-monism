import uuid


class UUIDGenerator:
    """UUID生成器类"""
    
    @staticmethod
    def uuid1():
        """生成基于时间戳和MAC地址的UUID"""
        return str(uuid.uuid1())
    
    @staticmethod
    def uuid3(namespace, name):
        """生成基于MD5哈希的UUID"""
        return str(uuid.uuid3(namespace, name))
    
    @staticmethod
    def uuid4():
        """生成随机UUID（最常用）"""
        return str(uuid.uuid4())
    
    @staticmethod
    def uuid5(namespace, name):
        """生成基于SHA-1哈希的UUID"""
        return str(uuid.uuid5(namespace, name))
    
    @staticmethod
    def uuid_hex():
        """生成不带连字符的UUID"""
        return uuid.uuid4().hex
    
    @staticmethod
    def uuid_bytes():
        """生成UUID的字节表示"""
        return uuid.uuid4().bytes


# 使用示例
if __name__ == "__main__":
    gen = UUIDGenerator()
    
    print("UUID1:", gen.uuid1())
    print("UUID4:", gen.uuid4())
    print("UUID Hex:", gen.uuid_hex())
    print("UUID3:", gen.uuid3(uuid.NAMESPACE_DNS, "example.com"))
    print("UUID5:", gen.uuid5(uuid.NAMESPACE_URL, "https://example.com"))