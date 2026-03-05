import re
from typing import Dict, Optional, Tuple


class UserRegistration:
    """用户注册管理类"""
    
    def __init__(self):
        self.users = {}
        self.username_index = set()
        self.email_index = set()
        self.next_user_id = 1
    
    def validate_username(self, username: Optional[str]) -> Tuple[bool, str]:
        """验证用户名"""
        if not username:
            return False, "用户名不能为空"
        
        if len(username) < 4 or len(username) > 20:
            return False, "用户名长度必须在4-20个字符之间"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "用户名只能包含字母、数字和下划线"
        
        return True, ""
    
    def validate_password(self, password: Optional[str]) -> Tuple[bool, str]:
        """验证密码"""
        if not password:
            return False, "密码不能为空"
        
        if len(password) < 6 or len(password) > 20:
            return False, "密码长度必须在6-20个字符之间"
        
        has_letter = bool(re.search(r'[a-zA-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        
        if not (has_letter and has_digit):
            return False, "密码必须同时包含字母和数字"
        
        return True, ""
    
    def validate_email(self, email: Optional[str]) -> Tuple[bool, str]:
        """验证邮箱格式"""
        if not email:
            return False, "邮箱不能为空"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "邮箱格式不正确"
        
        return True, ""
    
    def register(self, username: str, password: str, email: str) -> Dict:
        """用户注册主函数"""
        is_valid, error_msg = self.validate_username(username)
        if not is_valid:
            return {'success': False, 'error': error_msg}
        
        is_valid, error_msg = self.validate_password(password)
        if not is_valid:
            return {'success': False, 'error': error_msg}
        
        is_valid, error_msg = self.validate_email(email)
        if not is_valid:
            return {'success': False, 'error': error_msg}
        
        if username in self.username_index:
            return {'success': False, 'error': '用户名已存在'}
        
        if email in self.email_index:
            return {'success': False, 'error': '邮箱已被注册'}
        
        user_id = self.next_user_id
        self.users[user_id] = {
            'username': username,
            'password': password,
            'email': email
        }
        self.username_index.add(username)
        self.email_index.add(email)
        self.next_user_id += 1
        
        return {
            'success': True,
            'user_id': user_id,
            'username': username
        }
