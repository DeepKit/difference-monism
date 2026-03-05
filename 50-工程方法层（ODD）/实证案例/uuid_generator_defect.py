import uuid


class UUIDGenerator:
    @staticmethod
    def generate_uuid4():
        """生成随机UUID (最常用)"""
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_uuid1():
        """生成基于时间戳和MAC地址的UUID"""
        return str(uuid.uuid1())
    
    @staticmethod
    def generate_uuid3(namespace, name):
        """生成基于命名空间和名称的UUID (MD5)"""
        return str(uuid.uuid3(namespace, name))
    
    @staticmethod
    def generate_uuid5(namespace, name):
        """生成基于命名空间和名称的UUID (SHA-1)"""
        return str(uuid.uuid5(namespace, name))


# 使用示例
if __name__ == "__main__":
    gen = UUIDGenerator()
    
    # 随机UUID
    print(gen.generate_uuid4())
    
    # 时间戳UUID
    print(gen.generate_uuid1())
    
    # 命名空间UUID
    print(gen.generate_uuid5(uuid.NAMESPACE_DNS, "example.com"))