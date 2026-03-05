
import hmac
import hashlib
import time
import secrets
from typing import Dict, Optional
from urllib.parse import urlencode


class APISignature:
    """API签名工具类"""
    
    def __init__(self, secret_key: str, algorithm: str = 'sha256'):
        self.secret_key = secret_key.encode('utf-8')
        self.algorithm = algorithm
        self.hash_func = getattr(hashlib, algorithm)
    
    def generate_signature(
        self, 
        params: Dict[str, str], 
        method: str = 'GET',
        path: str = '',
        timestamp: Optional[int] = None,
        nonce: Optional[str] = None
    ) -> Dict[str, str]:
        """生成API签名"""
        if timestamp is None:
            timestamp = int(time.time())
        if nonce is None:
            nonce = secrets.token_hex(16)
        
        # 添加时间戳和随机数
        sign_params = params.copy()
        sign_params['timestamp'] = str(timestamp)
        sign_params['nonce'] = nonce
        
        # 构建签名字符串
        sign_string = self._build_sign_string(sign_params, method, path)
        
        # 生成签名
        signature = hmac.new(
            self.secret_key,
            sign_string.encode('utf-8'),
            self.hash_func
        ).hexdigest()
        
        sign_params['signature'] = signature
        return sign_params
    
    def verify_signature(
        self,
        params: Dict[str, str],
        method: str = 'GET',
        path: str = '',
        timeout: int = 300
    ) -> bool:
        """验证API签名"""
        if 'signature' not in params or 'timestamp' not in params:
            return False
        
        # 检查时间戳是否过期
        timestamp = int(params['timestamp'])
        if abs(int(time.time()) - timestamp) > timeout:
            return False
        
        # 提取并移除签名
        received_signature = params.pop('signature')
        
        # 重新计算签名
        sign_string = self._build_sign_string(params, method, path)
        expected_signature = hmac.new(
            self.secret_key,
            sign_string.encode('utf-8'),
            self.hash_func
        ).hexdigest()
        
        # 恢复签名参数
        params['signature'] = received_signature
        
        return hmac.compare_digest(received_signature, expected_signature)
    
    def _build_sign_string(
        self, 
        params: Dict[str, str], 
        method: str,
        path: str
    ) -> str:
        """构建待签名字符串"""
        # 参数按key排序
        sorted_params = sorted(params.items())
        query_string = urlencode(sorted_params)
        
        # 构建签名基础字符串: METHOD&PATH&QUERY_STRING
        return f"{method.upper()}&{path}&{query_string}"


# 使用示例
if __name__ == '__main__':
    # 初始化签名工具
    api_sig = APISignature(secret_key='your_secret_key_here')
    
    # 生成签名
    params = {
        'user_id': '12345',
        'action': 'get_profile'
    }
    signed_params = api_sig.generate_signature(
        params=params,
        method='GET',
        path='/api/user'
    )
    print("签名参数:", signed_params)
    
    # 验证签名
    is_valid = api_sig.verify_signature(
        params=signed_params,
        method='GET',
        path='/api/user'
    )
    print("签名验证:", "通过" if is_valid else "失败")
