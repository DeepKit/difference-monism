
import re
from typing import Optional


class DataMasker:
    """数据脱敏工具类"""
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """
        手机号脱敏：保留前3位和后4位
        例如：13812345678 -> 138****5678
        """
        if not phone or len(phone) < 11:
            return phone
        
        phone = re.sub(r'\D', '', phone)
        if len(phone) == 11:
            return f"{phone[:3]}****{phone[-4:]}"
        return phone
    
    @staticmethod
    def mask_email(email: str) -> str:
        """
        邮箱脱敏：保留第一个字符和@后的域名
        例如：example@gmail.com -> e****@gmail.com
        """
        if not email or '@' not in email:
            return email
        
        parts = email.split('@')
        if len(parts) != 2:
            return email
        
        username = parts[0]
        domain = parts[1]
        
        if len(username) <= 1:
            masked_username = username
        elif len(username) <= 3:
            masked_username = username[0] + '*' * (len(username) - 1)
        else:
            masked_username = username[0] + '****'
        
        return f"{masked_username}@{domain}"
    
    @staticmethod
    def mask_bank_card(card_number: str) -> str:
        """
        银行卡脱敏：保留前4位和后4位
        例如：6222021234567890 -> 6222********7890
        """
        if not card_number:
            return card_number
        
        card_number = re.sub(r'\s', '', card_number)
        
        if len(card_number) < 8:
            return card_number
        
        if len(card_number) <= 12:
            return f"{card_number[:4]}****{card_number[-4:]}"
        else:
            mask_length = len(card_number) - 8
            return f"{card_number[:4]}{'*' * mask_length}{card_number[-4:]}"
    
    def mask(self, data: str, data_type: str) -> str:
        """
        统一脱敏接口
        
        Args:
            data: 待脱敏的数据
            data_type: 数据类型 ('phone', 'email', 'bank_card')
        
        Returns:
            脱敏后的数据
        """
        maskers = {
            'phone': self.mask_phone,
            'email': self.mask_email,
            'bank_card': self.mask_bank_card
        }
        
        masker = maskers.get(data_type)
        if masker:
            return masker(data)
        return data


# 使用示例
if __name__ == '__main__':
    masker = DataMasker()
    
    # 手机号脱敏
    print(masker.mask_phone('13812345678'))  # 138****5678
    
    # 邮箱脱敏
    print(masker.mask_email('example@gmail.com'))  # e****@gmail.com
    
    # 银行卡脱敏
    print(masker.mask_bank_card('6222021234567890'))  # 6222********7890
    
    # 统一接口
    print(masker.mask('13812345678', 'phone'))
    print(masker.mask('test@example.com', 'email'))
    print(masker.mask('6222021234567890', 'bank_card'))
