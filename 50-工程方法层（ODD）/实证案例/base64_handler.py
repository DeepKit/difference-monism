import base64
from typing import Union, Optional
from pathlib import Path


class Base64Handler:
    """Base64编码解码处理类"""
    
    @staticmethod
    def encode_string(text: str, encoding: str = 'utf-8') -> str:
        """将字符串编码为Base64"""
        return base64.b64encode(text.encode(encoding)).decode('ascii')
    
    @staticmethod
    def decode_string(b64_text: str, encoding: str = 'utf-8') -> str:
        """将Base64解码为字符串"""
        return base64.b64decode(b64_text).decode(encoding)
    
    @staticmethod
    def encode_bytes(data: bytes) -> str:
        """将字节数据编码为Base64"""
        return base64.b64encode(data).decode('ascii')
    
    @staticmethod
    def decode_bytes(b64_text: str) -> bytes:
        """将Base64解码为字节数据"""
        return base64.b64decode(b64_text)
    
    @staticmethod
    def encode_file(file_path: Union[str, Path]) -> str:
        """将文件内容编码为Base64"""
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('ascii')
    
    @staticmethod
    def decode_to_file(b64_text: str, output_path: Union[str, Path]) -> None:
        """将Base64解码并保存为文件"""
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(b64_text))
    
    @staticmethod
    def encode_url_safe(text: str, encoding: str = 'utf-8') -> str:
        """URL安全的Base64编码"""
        return base64.urlsafe_b64encode(text.encode(encoding)).decode('ascii')
    
    @staticmethod
    def decode_url_safe(b64_text: str, encoding: str = 'utf-8') -> str:
        """URL安全的Base64解码"""
        return base64.urlsafe_b64decode(b64_text).decode(encoding)
    
    @staticmethod
    def is_valid_base64(b64_text: str) -> bool:
        """验证是否为有效的Base64字符串"""
        try:
            if isinstance(b64_text, str):
                b64_text = b64_text.encode('ascii')
            return base64.b64encode(base64.b64decode(b64_text)) == b64_text
        except Exception:
            return False
    
    @staticmethod
    def encode_with_padding(text: str, encoding: str = 'utf-8') -> str:
        """带填充的Base64编码"""
        encoded = base64.b64encode(text.encode(encoding)).decode('ascii')
        return encoded
    
    @staticmethod
    def decode_with_padding(b64_text: str, encoding: str = 'utf-8') -> str:
        """自动处理填充的Base64解码"""
        missing_padding = len(b64_text) % 4
        if missing_padding:
            b64_text += '=' * (4 - missing_padding)
        return base64.b64decode(b64_text).decode(encoding)


# 使用示例
if __name__ == '__main__':
    handler = Base64Handler()
    
    # 字符串编码解码
    text = "Hello, 世界!"
    encoded = handler.encode_string(text)
    decoded = handler.decode_string(encoded)
    print(f"原文: {text}")
    print(f"编码: {encoded}")
    print(f"解码: {decoded}")
    
    # URL安全编码
    url_encoded = handler.encode_url_safe(text)
    print(f"URL安全编码: {url_encoded}")
    
    # 验证Base64
    print(f"是否有效: {handler.is_valid_base64(encoded)}")