
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class JWTManager:
    """JWT令牌管理器"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """
        初始化JWT管理器
        
        Args:
            secret_key: 密钥
            algorithm: 加密算法，默认HS256
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def create_token(
        self, 
        payload: Dict[str, Any], 
        expires_in: int = 3600
    ) -> str:
        """
        创建JWT令牌
        
        Args:
            payload: 载荷数据
            expires_in: 过期时间（秒），默认1小时
            
        Returns:
            JWT令牌字符串
        """
        token_payload = payload.copy()
        
        # 添加标准声明
        now = datetime.utcnow()
        token_payload.update({
            "iat": now,  # 签发时间
            "exp": now + timedelta(seconds=expires_in),  # 过期时间
        })
        
        token = jwt.encode(
            token_payload, 
            self.secret_key, 
            algorithm=self.algorithm
        )
        
        return token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        验证并解码JWT令牌
        
        Args:
            token: JWT令牌字符串
            
        Returns:
            解码后的载荷数据，验证失败返回None
        """
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            print("令牌已过期")
            return None
        except jwt.InvalidTokenError:
            print("无效的令牌")
            return None
    
    def refresh_token(self, token: str, expires_in: int = 3600) -> Optional[str]:
        """
        刷新令牌
        
        Args:
            token: 原JWT令牌
            expires_in: 新令牌过期时间（秒）
            
        Returns:
            新的JWT令牌，验证失败返回None
        """
        payload = self.verify_token(token)
        if payload is None:
            return None
        
        # 移除时间相关的声明
        payload.pop("iat", None)
        payload.pop("exp", None)
        
        return self.create_token(payload, expires_in)


# 使用示例
if __name__ == "__main__":
    # 初始化JWT管理器
    jwt_manager = JWTManager(secret_key="your-secret-key-here")
    
    # 创建令牌
    user_data = {
        "user_id": 12345,
        "username": "john_doe",
        "role": "admin"
    }
    token = jwt_manager.create_token(user_data, expires_in=3600)
    print(f"生成的令牌: {token}")
    
    # 验证令牌
    decoded = jwt_manager.verify_token(token)
    print(f"解码的数据: {decoded}")
    
    # 刷新令牌
    new_token = jwt_manager.refresh_token(token, expires_in=7200)
    print(f"刷新后的令牌: {new_token}")
