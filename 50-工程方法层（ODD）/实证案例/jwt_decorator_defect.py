import jwt
from datetime import datetime, timedelta
from functools import wraps

class JWTAuthDecorator:
    def __init__(self, secret_key, algorithm='HS256', expiration_hours=24):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_hours = expiration_hours
    
    def generate_token(self, payload):
        """生成JWT token"""
        payload['exp'] = datetime.utcnow() + timedelta(hours=self.expiration_hours)
        payload['iat'] = datetime.utcnow()
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token):
        """验证JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload, None
        except jwt.ExpiredSignatureError:
            return None, "Token已过期"
        except jwt.InvalidTokenError:
            return None, "无效的Token"
    
    def require_auth(self, func):
        """装饰器：要求JWT认证"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 从kwargs中获取token，或从第一个参数获取
            token = kwargs.get('token') or (args[0] if args else None)
            
            if not token:
                raise ValueError("缺少认证Token")
            
            payload, error = self.verify_token(token)
            if error:
                raise ValueError(error)
            
            # 将payload注入到kwargs中
            kwargs['jwt_payload'] = payload
            return func(*args, **kwargs)
        
        return wrapper


# 使用示例
if __name__ == "__main__":
    # 初始化
    jwt_auth = JWTAuthDecorator(secret_key="your-secret-key")
    
    # 生成token
    token = jwt_auth.generate_token({"user_id": 123, "username": "test_user"})
    print(f"生成的Token: {token}")
    
    # 使用装饰器保护函数
    @jwt_auth.require_auth
    def protected_function(token, jwt_payload=None):
        print(f"认证成功! 用户信息: {jwt_payload}")
        return "访问受保护的资源"
    
    # 调用受保护的函数
    try:
        result = protected_function(token=token)
        print(result)
    except ValueError as e:
        print(f"认证失败: {e}")