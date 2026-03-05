
import re
import hashlib
from typing import Optional, Callable
from enum import Enum


class MaskStrategy(Enum):
    """脱敏策略枚举"""
    PARTIAL = "partial"  # 部分掩码
    FULL = "full"  # 完全掩码
    HASH = "hash"  # 哈希处理


class DataMasker:
    """数据脱敏处理类"""
    
    def __init__(self, mask_char: str = "*"):
        self.mask_char = mask_char
    
    def mask_phone(self, phone: str, keep_start: int = 3, keep_end: int = 4) -> str:
        """手机号脱敏：保留前3位和后4位"""
        if not phone or len(phone) < keep_start + keep_end:
            return phone
        return phone[:keep_start] + self.mask_char * (len(phone) - keep_start - keep_end) + phone[-keep_end:]
    
    def mask_email(self, email: str, keep_start: int = 2) -> str:
        """邮箱脱敏：保留前2位和@后的域名"""
        if not email or '@' not in email:
            return email
        local, domain = email.split('@', 1)
        if len(local) <= keep_start:
            masked_local = self.mask_char * len(local)
        else:
            masked_local = local[:keep_start] + self.mask_char * (len(local) - keep_start)
        return f"{masked_local}@{domain}"
    
    def mask_id_card(self, id_card: str, keep_start: int = 6, keep_end: int = 4) -> str:
        """身份证号脱敏：保留前6位和后4位"""
        if not id_card or len(id_card) < keep_start + keep_end:
            return id_card
        return id_card[:keep_start] + self.mask_char * (len(id_card) - keep_start - keep_end) + id_card[-keep_end:]
    
    def mask_bank_card(self, card: str, keep_start: int = 4, keep_end: int = 4) -> str:
        """银行卡号脱敏：保留前4位和后4位"""
        if not card or len(card) < keep_start + keep_end:
            return card
        return card[:keep_start] + self.mask_char * (len(card) - keep_start - keep_end) + card[-keep_end:]
    
    def mask_name(self, name: str) -> str:
        """姓名脱敏：保留姓氏"""
        if not name or len(name) < 2:
            return self.mask_char * len(name) if name else ""
        return name[0] + self.mask_char * (len(name) - 1)
    
    def mask_address(self, address: str, keep_length: int = 6) -> str:
        """地址脱敏：保留前几位"""
        if not address or len(address) <= keep_length:
            return address
        return address[:keep_length] + self.mask_char * (len(address) - keep_length)
    
    def mask_custom(self, text: str, keep_start: int = 0, keep_end: int = 0) -> str:
        """自定义脱敏规则"""
        if not text or len(text) <= keep_start + keep_end:
            return text
        if keep_start == 0 and keep_end == 0:
            return self.mask_char * len(text)
        return text[:keep_start] + self.mask_char * (len(text) - keep_start - keep_end) + text[-keep_end:] if keep_end > 0 else text[:keep_start] + self.mask_char * (len(text) - keep_start)
    
    def hash_data(self, data: str, algorithm: str = "sha256") -> str:
        """哈希处理敏感数据"""
        if not data:
            return ""
        hash_func = getattr(hashlib, algorithm)
        return hash_func(data.encode()).hexdigest()


class SensitiveDataProcessor:
    """敏感数据处理器"""
    
    def __init__(self, masker: Optional[DataMasker] = None):
        self.masker = masker or DataMasker()
        self.patterns = {
            'phone': re.compile(r'1[3-9]\d{9}'),
            'email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            'id_card': re.compile(r'\d{17}[\dXx]|\d{15}'),
            'bank_card': re.compile(r'\d{16,19}'),
        }
    
    def detect_and_mask(self, text: str, data_type: Optional[str] = None) -> str:
        """自动检测并脱敏文本中的敏感信息"""
        if data_type:
            return self._mask_by_type(text, data_type)
        
        result = text
        for dtype, pattern in self.patterns.items():
            result = pattern.sub(lambda m: self._mask_by_type(m.group(), dtype), result)
        return result
    
    def _mask_by_type(self, text: str, data_type: str) -> str:
        """根据类型进行脱敏"""
        mask_methods = {
            'phone': self.masker.mask_phone,
            'email': self.masker.mask_email,
            'id_card': self.masker.mask_id_card,
            'bank_card': self.masker.mask_bank_card,
            'name': self.masker.mask_name,
            'address': self.masker.mask_address,
        }
        method = mask_methods.get(data_type)
        return method(text) if method else text
    
    def mask_dict(self, data: dict, rules: dict) -> dict:
        """对字典数据按规则脱敏"""
        result = {}
        for key, value in data.items():
            if key in rules:
                rule = rules[key]
                if isinstance(rule, str):
                    result[key] = self._mask_by_type(str(value), rule)
                elif callable(rule):
                    result[key] = rule(value)
                else:
                    result[key] = value
            else:
                result[key] = value
        return result
    
    def mask_list(self, data: list, mask_func: Callable) -> list:
        """对列表数据批量脱敏"""
        return [mask_func(item) for item in data]


class AdvancedMasker:
    """高级脱敏功能"""
    
    @staticmethod
    def reversible_mask(data: str, key: str) -> tuple[str, str]:
        """可逆脱敏（简单异或加密）"""
        key_bytes = key.encode()
        data_bytes = data.encode()
        masked = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data_bytes)])
        return masked.hex(), key
    
    @staticmethod
    def reversible_unmask(masked_hex: str, key: str) -> str:
        """解密可逆脱敏数据"""
        key_bytes = key.encode()
        masked_bytes = bytes.fromhex(masked_hex)
        original = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(masked_bytes)])
        return original.decode()
    
    @staticmethod
    def tokenize(data: str, salt: str = "") -> str:
        """令牌化处理"""
        return hashlib.sha256((data + salt).encode()).hexdigest()[:16]


# 使用示例
if __name__ == "__main__":
    # 基础脱敏
    masker = DataMasker()
    print(masker.mask_phone("13812345678"))
    print(masker.mask_email("user@example.com"))
    print(masker.mask_id_card("110101199001011234"))
    print(masker.mask_bank_card("6222021234567890123"))
    print(masker.mask_name("张三"))
    print(masker.mask_address("北京市朝阳区某某街道123号"))
    
    # 自动检测脱敏
    processor = SensitiveDataProcessor()
    text = "联系方式：13812345678，邮箱：user@example.com"
    print(processor.detect_and_mask(text))
    
    # 字典数据脱敏
    user_data = {
        "name": "李四",
        "phone": "13987654321",
        "email": "lisi@example.com",
        "age": 30
    }
    rules = {
        "name": "name",
        "phone": "phone",
        "email": "email"
    }
    print(processor.mask_dict(user_data, rules))
    
    # 哈希处理
    print(masker.hash_data("sensitive_data"))
    
    # 可逆脱敏
    masked, key = AdvancedMasker.reversible_mask("敏感信息", "secret_key")
    print(f"加密: {masked}")
    print(f"解密: {AdvancedMasker.reversible_unmask(masked, key)}")
