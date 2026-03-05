
import hmac
import hashlib
import time
from typing import Optional


class APISignatureValidator:
    def __init__(self, secret_key: str, time_window: int = 300):
        """
        初始化API签名验证器
        
        :param secret_key: 密钥
        :param time_window: 时间窗口（秒），默认5分钟
        """
        self.secret_key = secret_key.encode('utf-8')
        self.time_window = time_window
    
    def generate_signature(self, data: str, timestamp: int) -> str:
        """
        生成HMAC-SHA256签名
        
        :param data: 待签名数据
        :param timestamp: 时间戳
        :return: 签名字符串
        """
        message = f"{data}{timestamp}".encode('utf-8')
        signature = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
        return signature
    
    def validate_timestamp(self, timestamp: int) -> bool:
        """
        验证时间戳是否在有效窗口内
        
        :param timestamp: 请求时间戳
        :return: 是否有效
        """
        current_time = int(time.time())
        time_diff = abs(current_time - timestamp)
        return time_diff <= self.time_window
    
    def validate_signature(self, data: str, timestamp: int, signature: str) -> bool:
        """
        验证签名和时间戳
        
        :param data: 原始数据
        :param timestamp: 时间戳
        :param signature: 待验证的签名
        :return: 验证是否通过
        """
        if not self.validate_timestamp(timestamp):
            return False
        
        expected_signature = self.generate_signature(data, timestamp)
        return hmac.compare_digest(expected_signature, signature)
    
    def create_signed_request(self, data: str) -> dict:
        """
        创建带签名的请求
        
        :param data: 请求数据
        :return: 包含数据、时间戳和签名的字典
        """
        timestamp = int(time.time())
        signature = self.generate_signature(data, timestamp)
        return {
            'data': data,
            'timestamp': timestamp,
            'signature': signature
        }
