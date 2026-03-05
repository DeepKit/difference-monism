import hashlib
from pathlib import Path
from typing import Union, Literal

HashAlgorithm = Literal['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s']


class HashGenerator:
    """哈希生成器类"""
    
    def __init__(self, algorithm: HashAlgorithm = 'sha256'):
        """
        初始化哈希生成器
        
        Args:
            algorithm: 哈希算法，默认为sha256
        """
        self.algorithm = algorithm.lower()
        self._validate_algorithm()
    
    def _validate_algorithm(self):
        """验证算法是否支持"""
        try:
            hashlib.new(self.algorithm)
        except ValueError:
            raise ValueError(f"不支持的哈希算法: {self.algorithm}")
    
    def hash_string(self, text: str, encoding: str = 'utf-8') -> str:
        """
        生成字符串的哈希值
        
        Args:
            text: 要哈希的字符串
            encoding: 字符编码，默认utf-8
            
        Returns:
            十六进制哈希值
        """
        hasher = hashlib.new(self.algorithm)
        hasher.update(text.encode(encoding))
        return hasher.hexdigest()
    
    def hash_bytes(self, data: bytes) -> str:
        """
        生成字节数据的哈希值
        
        Args:
            data: 要哈希的字节数据
            
        Returns:
            十六进制哈希值
        """
        hasher = hashlib.new(self.algorithm)
        hasher.update(data)
        return hasher.hexdigest()
    
    def hash_file(self, filepath: Union[str, Path], chunk_size: int = 8192) -> str:
        """
        生成文件的哈希值
        
        Args:
            filepath: 文件路径
            chunk_size: 读取块大小，默认8192字节
            
        Returns:
            十六进制哈希值
        """
        hasher = hashlib.new(self.algorithm)
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    @staticmethod
    def quick_hash(text: str, algorithm: HashAlgorithm = 'sha256') -> str:
        """
        快速生成字符串哈希值（静态方法）
        
        Args:
            text: 要哈希的字符串
            algorithm: 哈希算法
            
        Returns:
            十六进制哈希值
        """
        return hashlib.new(algorithm, text.encode()).hexdigest()
    
    def compare(self, text: str, hash_value: str) -> bool:
        """
        比较文本的哈希值是否匹配
        
        Args:
            text: 要验证的文本
            hash_value: 预期的哈希值
            
        Returns:
            是否匹配
        """
        return self.hash_string(text) == hash_value.lower()


# 使用示例
if __name__ == '__main__':
    # 创建哈希生成器
    gen = HashGenerator('sha256')
    
    # 哈希字符串
    text = "Hello, World!"
    hash_result = gen.hash_string(text)
    print(f"SHA256: {hash_result}")
    
    # 使用不同算法
    md5_gen = HashGenerator('md5')
    print(f"MD5: {md5_gen.hash_string(text)}")
    
    # 快速哈希
    quick = HashGenerator.quick_hash(text, 'sha1')
    print(f"SHA1: {quick}")
    
    # 验证哈希
    is_match = gen.compare(text, hash_result)
    print(f"验证结果: {is_match}")