import re
from typing import Optional


class DataMaskerV2:
    """数据脱敏工具类"""
    
    @staticmethod
    def phone(phone: str, mask_char: str = '*') -> str:
        """手机号脱敏：保留前3位和后4位"""
        if not phone or len(phone) < 7:
            return phone
        return phone[:3] + mask_char * 4 + phone[-4:]
    
    @staticmethod
    def id_card(id_card: str, mask_char: str = '*') -> str:
        """身份证号脱敏：保留前6位和后4位"""
        if not id_card or len(id_card) < 10:
            return id_card
        return id_card[:6] + mask_char * (len(id_card) - 10) + id_card[-4:]
    
    @staticmethod
    def email(email: str, mask_char: str = '*') -> str:
        """邮箱脱敏：保留前2位和@后的域名"""
        if not email or '@' not in email:
            return email
        parts = email.split('@')
        username = parts[0]
        if len(username) <= 2:
            return email
        return username[:2] + mask_char * (len(username) - 2) + '@' + parts[1]
    
    @staticmethod
    def name(name: str, mask_char: str = '*') -> str:
        """姓名脱敏：保留姓氏"""
        if not name or len(name) < 2:
            return name
        return name[0] + mask_char * (len(name) - 1)
    
    @staticmethod
    def bank_card(card: str, mask_char: str = '*') -> str:
        """银行卡号脱敏：保留前4位和后4位"""
        if not card or len(card) < 8:
            return card
        return card[:4] + mask_char * (len(card) - 8) + card[-4:]
    
    @staticmethod
    def address(address: str, mask_char: str = '*', keep_length: int = 6) -> str:
        """地址脱敏：保留前N位"""
        if not address or len(address) <= keep_length:
            return address
        return address[:keep_length] + mask_char * (len(address) - keep_length)
    
    @staticmethod
    def custom(text: str, start: int, end: int, mask_char: str = '*') -> str:
        """自定义脱敏：指定保留开始和结束位数"""
        if not text or len(text) <= start + end:
            return text
        return text[:start] + mask_char * (len(text) - start - end) + text[-end:] if end > 0 else text[:start] + mask_char * (len(text) - start)


# 使用示例
if __name__ == '__main__':
    masker = DataMaskerV2()
    
    print(masker.phone('13812345678'))           # 138****5678
    print(masker.id_card('110101199001011234'))  # 110101********1234
    print(masker.email('example@gmail.com'))     # ex*****@gmail.com
    print(masker.name('张三'))                    # 张*
    print(masker.bank_card('6222021234567890'))  # 6222********7890
    print(masker.address('北京市朝阳区某某街道123号'))  # 北京市朝阳区******