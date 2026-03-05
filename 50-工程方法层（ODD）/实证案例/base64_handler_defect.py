import base64


class Base64Handler:
    @staticmethod
    def encode(data: str | bytes) -> str:
        """编码为Base64字符串"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')
    
    @staticmethod
    def decode(data: str) -> str:
        """解码Base64字符串"""
        return base64.b64decode(data).decode('utf-8')
    
    @staticmethod
    def decode_to_bytes(data: str) -> bytes:
        """解码Base64字符串为字节"""
        return base64.b64decode(data)
    
    @staticmethod
    def encode_url_safe(data: str | bytes) -> str:
        """URL安全的Base64编码"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.urlsafe_b64encode(data).decode('utf-8')
    
    @staticmethod
    def decode_url_safe(data: str) -> str:
        """URL安全的Base64解码"""
        return base64.urlsafe_b64decode(data).decode('utf-8')


# 使用示例
if __name__ == '__main__':
    handler = Base64Handler()
    
    # 编码
    encoded = handler.encode("Hello, World!")
    print(f"编码: {encoded}")
    
    # 解码
    decoded = handler.decode(encoded)
    print(f"解码: {decoded}")