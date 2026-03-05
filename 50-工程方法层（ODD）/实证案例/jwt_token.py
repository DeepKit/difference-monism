
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in: int


class JWTTokenManager:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 7
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def generate_access_token(self, payload: Dict[str, Any]) -> str:
        """生成访问令牌"""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        token_payload = {
            **payload,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(token_payload, self.secret_key, algorithm=self.algorithm)

    def generate_refresh_token(self, payload: Dict[str, Any]) -> str:
        """生成刷新令牌"""
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        token_payload = {
            **payload,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(token_payload, self.secret_key, algorithm=self.algorithm)

    def generate_token_pair(self, payload: Dict[str, Any]) -> TokenPair:
        """生成访问令牌和刷新令牌对"""
        access_token = self.generate_access_token(payload)
        refresh_token = self.generate_refresh_token(payload)
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.access_token_expire_minutes * 60
        )

    def verify_token(self, token: str, token_type: Optional[str] = None) -> Dict[str, Any]:
        """验证令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if token_type and payload.get("type") != token_type:
                raise jwt.InvalidTokenError(f"Invalid token type. Expected {token_type}")
            
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """验证访问令牌"""
        return self.verify_token(token, token_type="access")

    def verify_refresh_token(self, token: str) -> Dict[str, Any]:
        """验证刷新令牌"""
        return self.verify_token(token, token_type="refresh")

    def refresh_access_token(self, refresh_token: str) -> str:
        """使用刷新令牌生成新的访问令牌"""
        payload = self.verify_refresh_token(refresh_token)
        
        # 移除JWT标准字段
        user_payload = {k: v for k, v in payload.items() 
                       if k not in ["exp", "iat", "type"]}
        
        return self.generate_access_token(user_payload)

    def decode_token_without_verification(self, token: str) -> Dict[str, Any]:
        """解码令牌但不验证（用于调试）"""
        return jwt.decode(token, options={"verify_signature": False})


# 使用示例
if __name__ == "__main__":
    # 初始化管理器
    token_manager = JWTTokenManager(
        secret_key="your-secret-key-here",
        access_token_expire_minutes=15,
        refresh_token_expire_days=7
    )
    
    # 生成令牌对
    user_data = {"user_id": 123, "username": "john_doe", "role": "admin"}
    tokens = token_manager.generate_token_pair(user_data)
    
    print(f"Access Token: {tokens.access_token}")
    print(f"Refresh Token: {tokens.refresh_token}")
    print(f"Expires In: {tokens.expires_in} seconds")
    
    # 验证访问令牌
    try:
        payload = token_manager.verify_access_token(tokens.access_token)
        print(f"\nVerified Payload: {payload}")
    except ValueError as e:
        print(f"Verification failed: {e}")
    
    # 刷新访问令牌
    try:
        new_access_token = token_manager.refresh_access_token(tokens.refresh_token)
        print(f"\nNew Access Token: {new_access_token}")
    except ValueError as e:
        print(f"Refresh failed: {e}")
