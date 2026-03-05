import re
from typing import Optional


class PhoneFormatter:
    """电话号码格式化类"""
    
    def __init__(self, default_country_code: str = "+1"):
        """
        初始化格式化器
        
        Args:
            default_country_code: 默认国家代码，如 "+1" (美国), "+86" (中国)
        """
        self.default_country_code = default_country_code
    
    def clean(self, phone: str) -> str:
        """
        清理电话号码，只保留数字和+号
        
        Args:
            phone: 原始电话号码
            
        Returns:
            清理后的电话号码
        """
        return re.sub(r'[^\d+]', '', phone)
    
    def format_us(self, phone: str) -> Optional[str]:
        """
        格式化为美国格式: (123) 456-7890
        
        Args:
            phone: 电话号码
            
        Returns:
            格式化后的电话号码，无效则返回None
        """
        digits = self.clean(phone).lstrip('+').lstrip('1')
        
        if len(digits) != 10:
            return None
        
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    
    def format_international(self, phone: str, country_code: Optional[str] = None) -> Optional[str]:
        """
        格式化为国际格式: +1 123 456 7890
        
        Args:
            phone: 电话号码
            country_code: 国家代码，如不提供则使用默认值
            
        Returns:
            格式化后的电话号码
        """
        cleaned = self.clean(phone)
        
        if not cleaned:
            return None
        
        # 如果已有+号，直接使用
        if cleaned.startswith('+'):
            digits = cleaned[1:]
            code = '+' + digits[:len(self.default_country_code) - 1]
            number = digits[len(self.default_country_code) - 1:]
        else:
            code = country_code or self.default_country_code
            digits = cleaned.lstrip('0')
            number = digits
        
        # 按3-3-4格式分组
        if len(number) >= 10:
            return f"{code} {number[:3]} {number[3:6]} {number[6:]}"
        else:
            return f"{code} {number}"
    
    def format_dashed(self, phone: str) -> Optional[str]:
        """
        格式化为连字符格式: 123-456-7890
        
        Args:
            phone: 电话号码
            
        Returns:
            格式化后的电话号码
        """
        digits = self.clean(phone).lstrip('+').lstrip('1')
        
        if len(digits) != 10:
            return None
        
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    
    def format_dotted(self, phone: str) -> Optional[str]:
        """
        格式化为点分格式: 123.456.7890
        
        Args:
            phone: 电话号码
            
        Returns:
            格式化后的电话号码
        """
        digits = self.clean(phone).lstrip('+').lstrip('1')
        
        if len(digits) != 10:
            return None
        
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:]}"
    
    def format_chinese(self, phone: str) -> Optional[str]:
        """
        格式化为中国格式: 138 1234 5678
        
        Args:
            phone: 电话号码
            
        Returns:
            格式化后的电话号码
        """
        digits = self.clean(phone).lstrip('+').lstrip('86')
        
        if len(digits) != 11:
            return None
        
        return f"{digits[:3]} {digits[3:7]} {digits[7:]}"
    
    def validate(self, phone: str, min_length: int = 10, max_length: int = 15) -> bool:
        """
        验证电话号码是否有效
        
        Args:
            phone: 电话号码
            min_length: 最小长度
            max_length: 最大长度
            
        Returns:
            是否有效
        """
        digits = self.clean(phone).lstrip('+')
        return min_length <= len(digits) <= max_length
    
    def get_digits_only(self, phone: str) -> str:
        """
        获取纯数字格式
        
        Args:
            phone: 电话号码
            
        Returns:
            纯数字字符串
        """
        return self.clean(phone).lstrip('+')


# 使用示例
if __name__ == "__main__":
    formatter = PhoneFormatter()
    
    # 测试各种格式
    test_phones = [
        "1234567890",
        "+1 (123) 456-7890",
        "123.456.7890",
        "+86 138 1234 5678"
    ]
    
    for phone in test_phones:
        print(f"\n原始: {phone}")
        print(f"美国格式: {formatter.format_us(phone)}")
        print(f"国际格式: {formatter.format_international(phone)}")
        print(f"连字符: {formatter.format_dashed(phone)}")
        print(f"纯数字: {formatter.get_digits_only(phone)}")
        print(f"有效性: {formatter.validate(phone)}")