import re
from typing import Dict, Optional


class RegistrationError(Exception):
    """注册错误基类"""
    pass


class UserRegistry:
    """用户注册管理类"""
    
    def __init__(self):
        # 使用小写邮箱作为键，存储用户信息
        self._users: Dict[str, dict] = {}
    
    def register(self, email: str, password: str) -> dict:
        """
        注册新用户
        
        Args:
            email: 用户邮箱
            password: 用户密码
            
        Returns:
            注册成功的用户信息
            
        Raises:
            RegistrationError: 注册失败时抛出，包含具体错误信息
        """
        # 验证邮箱格式
        if not self._is_valid_email(email):
            raise RegistrationError("邮箱格式不正确")
        
        # 检查重复注册（大小写不敏感）
        email_lower = email.lower()
        if email_lower in self._users:
            raise RegistrationError("该邮箱已被注册")
        
        # 验证密码
        password_error = self._validate_password(password)
        if password_error:
            raise RegistrationError(password_error)
        
        # 注册成功，存储用户信息
        user_info = {
            "email": email,
            "email_lower": email_lower
        }
        self._users[email_lower] = user_info
        
        return {"email": email, "status": "registered"}
    
    def _is_valid_email(self, email: str) -> bool:
        """验证邮箱格式"""
        if not email:
            return False
        
        # 基本的邮箱格式验证
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_password(self, password: str) -> Optional[str]:
        """
        验证密码强度
        
        Returns:
            如果密码有效返回None，否则返回错误信息
        """
        if not password:
            return "密码不能为空"
        
        if len(password) < 8:
            return "密码长度至少为8位"
        
        # 检查是否包含数字
        has_digit = any(c.isdigit() for c in password)
        if not has_digit:
            return "密码必须包含至少一个数字"
        
        # 检查是否包含字母
        has_letter = any(c.isalpha() for c in password)
        if not has_letter:
            return "密码必须包含至少一个字母"
        
        return None
    
    def is_registered(self, email: str) -> bool:
        """检查邮箱是否已注册"""
        return email.lower() in self._users
    
    def get_user_count(self) -> int:
        """获取已注册用户数量"""
        return len(self._users)
