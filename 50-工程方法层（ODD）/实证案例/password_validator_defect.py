import re

class PasswordValidator:
    def __init__(self, min_length=8, require_uppercase=True, require_lowercase=True, 
                 require_digit=True, require_special=True):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
    
    def validate(self, password):
        """验证密码，返回(是否有效, 错误信息列表)"""
        errors = []
        
        if len(password) < self.min_length:
            errors.append(f"密码长度至少需要{self.min_length}个字符")
        
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("密码必须包含至少一个大写字母")
        
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("密码必须包含至少一个小写字母")
        
        if self.require_digit and not re.search(r'\d', password):
            errors.append("密码必须包含至少一个数字")
        
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("密码必须包含至少一个特殊字符")
        
        return len(errors) == 0, errors
    
    def is_valid(self, password):
        """快速检查密码是否有效"""
        return self.validate(password)[0]


# 使用示例
if __name__ == "__main__":
    validator = PasswordValidator(min_length=8)
    
    test_passwords = ["weak", "Strong123", "Strong123!"]
    
    for pwd in test_passwords:
        is_valid, errors = validator.validate(pwd)
        print(f"密码: {pwd}")
        print(f"有效: {is_valid}")
        if errors:
            print(f"错误: {', '.join(errors)}")
        print()