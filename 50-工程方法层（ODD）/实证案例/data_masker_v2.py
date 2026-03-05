import re
import hashlib
import secrets
from typing import Optional, Union, Dict, List, Callable
from enum import Enum
from dataclasses import dataclass


class MaskingStrategy(Enum):
    """脱敏策略枚举"""
    FULL = "full"  # 完全脱敏
    PARTIAL = "partial"  # 部分脱敏
    HASH = "hash"  # 哈希脱敏
    TOKENIZE = "tokenize"  # 令牌化


@dataclass
class MaskingConfig:
    """脱敏配置"""
    strategy: MaskingStrategy = MaskingStrategy.PARTIAL
    mask_char: str = "*"
    keep_prefix: int = 3
    keep_suffix: int = 4
    hash_algorithm: str = "sha256"


class DataMaskerV2:
    """数据脱敏类V2 - 支持多种PII数据类型的脱敏"""
    
    def __init__(self, default_config: Optional[MaskingConfig] = None):
        """
        初始化数据脱敏器
        
        Args:
            default_config: 默认脱敏配置
        """
        self.default_config = default_config or MaskingConfig()
        self._token_map: Dict[str, str] = {}
        
        # 正则表达式模式
        self.patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone_cn': r'^1[3-9]\d{9}$',
            'phone_intl': r'^\+?[1-9]\d{1,14}$',
            'credit_card': r'^\d{13,19}$',
            'ssn': r'^\d{3}-?\d{2}-?\d{4}$',
            'id_card_cn': r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$',
            'ip_v4': r'^(\d{1,3}\.){3}\d{1,3}$',
            'ip_v6': r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
        }
    
    def mask(self, data: Union[str, Dict, List], 
             data_type: Optional[str] = None,
             config: Optional[MaskingConfig] = None) -> Union[str, Dict, List]:
        """
        通用脱敏方法
        
        Args:
            data: 待脱敏数据
            data_type: 数据类型 (email, phone, credit_card等)
            config: 脱敏配置
            
        Returns:
            脱敏后的数据
        """
        if data is None:
            return None
            
        config = config or self.default_config
        
        try:
            if isinstance(data, dict):
                return self._mask_dict(data, config)
            elif isinstance(data, list):
                return self._mask_list(data, config)
            elif isinstance(data, str):
                if not data.strip():
                    return data
                return self._mask_string(data, data_type, config)
            else:
                raise ValueError(f"不支持的数据类型: {type(data)}")
        except Exception as e:
            raise RuntimeError(f"脱敏失败: {str(e)}")
    
    def mask_email(self, email: str, config: Optional[MaskingConfig] = None) -> str:
        """脱敏邮箱地址"""
        if not email or not isinstance(email, str):
            raise ValueError("邮箱地址不能为空且必须是字符串")
        
        if not re.match(self.patterns['email'], email):
            raise ValueError(f"无效的邮箱格式: {email}")
        
        config = config or self.default_config
        
        try:
            local, domain = email.split('@')
            
            if config.strategy == MaskingStrategy.FULL:
                return f"{config.mask_char * len(local)}@{domain}"
            elif config.strategy == MaskingStrategy.PARTIAL:
                if len(local) <= 2:
                    masked_local = config.mask_char * len(local)
                else:
                    keep = min(config.keep_prefix, len(local) - 1)
                    masked_local = local[:keep] + config.mask_char * (len(local) - keep)
                return f"{masked_local}@{domain}"
            elif config.strategy == MaskingStrategy.HASH:
                return self._hash_data(email, config)
            elif config.strategy == MaskingStrategy.TOKENIZE:
                return self._tokenize(email)
        except Exception as e:
            raise RuntimeError(f"邮箱脱敏失败: {str(e)}")
    
    def mask_phone(self, phone: str, config: Optional[MaskingConfig] = None) -> str:
        """脱敏手机号"""
        if not phone or not isinstance(phone, str):
            raise ValueError("手机号不能为空且必须是字符串")
        
        phone = phone.strip().replace(' ', '').replace('-', '')
        
        if not (re.match(self.patterns['phone_cn'], phone) or 
                re.match(self.patterns['phone_intl'], phone)):
            raise ValueError(f"无效的手机号格式: {phone}")
        
        config = config or self.default_config
        
        try:
            if config.strategy == MaskingStrategy.FULL:
                return config.mask_char * len(phone)
            elif config.strategy == MaskingStrategy.PARTIAL:
                if len(phone) <= 7:
                    return phone[:3] + config.mask_char * (len(phone) - 3)
                return phone[:3] + config.mask_char * (len(phone) - 7) + phone[-4:]
            elif config.strategy == MaskingStrategy.HASH:
                return self._hash_data(phone, config)
            elif config.strategy == MaskingStrategy.TOKENIZE:
                return self._tokenize(phone)
        except Exception as e:
            raise RuntimeError(f"手机号脱敏失败: {str(e)}")
    
    def mask_credit_card(self, card_number: str, config: Optional[MaskingConfig] = None) -> str:
        """脱敏信用卡号"""
        if not card_number or not isinstance(card_number, str):
            raise ValueError("信用卡号不能为空且必须是字符串")
        
        card_number = card_number.strip().replace(' ', '').replace('-', '')
        
        if not re.match(self.patterns['credit_card'], card_number):
            raise ValueError(f"无效的信用卡号格式: {card_number}")
        
        config = config or self.default_config
        
        try:
            if config.strategy == MaskingStrategy.FULL:
                return config.mask_char * len(card_number)
            elif config.strategy == MaskingStrategy.PARTIAL:
                return card_number[:6] + config.mask_char * (len(card_number) - 10) + card_number[-4:]
            elif config.strategy == MaskingStrategy.HASH:
                return self._hash_data(card_number, config)
            elif config.strategy == MaskingStrategy.TOKENIZE:
                return self._tokenize(card_number)
        except Exception as e:
            raise RuntimeError(f"信用卡号脱敏失败: {str(e)}")
    
    def mask_id_card(self, id_card: str, config: Optional[MaskingConfig] = None) -> str:
        """脱敏身份证号"""
        if not id_card or not isinstance(id_card, str):
            raise ValueError("身份证号不能为空且必须是字符串")
        
        id_card = id_card.strip().upper()
        
        if not re.match(self.patterns['id_card_cn'], id_card):
            raise ValueError(f"无效的身份证号格式: {id_card}")
        
        config = config or self.default_config
        
        try:
            if config.strategy == MaskingStrategy.FULL:
                return config.mask_char * len(id_card)
            elif config.strategy == MaskingStrategy.PARTIAL:
                return id_card[:6] + config.mask_char * (len(id_card) - 10) + id_card[-4:]
            elif config.strategy == MaskingStrategy.HASH:
                return self._hash_data(id_card, config)
            elif config.strategy == MaskingStrategy.TOKENIZE:
                return self._tokenize(id_card)
        except Exception as e:
            raise RuntimeError(f"身份证号脱敏失败: {str(e)}")
    
    def mask_name(self, name: str, config: Optional[MaskingConfig] = None) -> str:
        """脱敏姓名"""
        if not name or not isinstance(name, str):
            raise ValueError("姓名不能为空且必须是字符串")
        
        name = name.strip()
        config = config or self.default_config
        
        try:
            if config.strategy == MaskingStrategy.FULL:
                return config.mask_char * len(name)
            elif config.strategy == MaskingStrategy.PARTIAL:
                if len(name) <= 1:
                    return config.mask_char
                elif len(name) == 2:
                    return name[0] + config.mask_char
                else:
                    return name[0] + config.mask_char * (len(name) - 1)
            elif config.strategy == MaskingStrategy.HASH:
                return self._hash_data(name, config)
            elif config.strategy == MaskingStrategy.TOKENIZE:
                return self._tokenize(name)
        except Exception as e:
            raise RuntimeError(f"姓名脱敏失败: {str(e)}")
    
    def mask_ip(self, ip: str, config: Optional[MaskingConfig] = None) -> str:
        """脱敏IP地址"""
        if not ip or not isinstance(ip, str):
            raise ValueError("IP地址不能为空且必须是字符串")
        
        ip = ip.strip()
        
        if not (re.match(self.patterns['ip_v4'], ip) or 
                re.match(self.patterns['ip_v6'], ip)):
            raise ValueError(f"无效的IP地址格式: {ip}")
        
        config = config or self.default_config
        
        try:
            if config.strategy == MaskingStrategy.FULL:
                return config.mask_char * len(ip)
            elif config.strategy == MaskingStrategy.PARTIAL:
                if '.' in ip:  # IPv4
                    parts = ip.split('.')
                    return f"{parts[0]}.{parts[1]}.{config.mask_char * len(parts[2])}.{config.mask_char * len(parts[3])}"
                else:  # IPv6
                    parts = ip.split(':')
                    return ':'.join(parts[:4] + [config.mask_char * 4] * (len(parts) - 4))
            elif config.strategy == MaskingStrategy.HASH:
                return self._hash_data(ip, config)
            elif config.strategy == MaskingStrategy.TOKENIZE:
                return self._tokenize(ip)
        except Exception as e:
            raise RuntimeError(f"IP地址脱敏失败: {str(e)}")
    
    def mask_custom(self, data: str, mask_func: Callable[[str], str]) -> str:
        """自定义脱敏方法"""
        if not data or not isinstance(data, str):
            raise ValueError("数据不能为空且必须是字符串")
        
        if not callable(mask_func):
            raise ValueError("mask_func必须是可调用对象")
        
        try:
            return mask_func(data)
        except Exception as e:
            raise RuntimeError(f"自定义脱敏失败: {str(e)}")
    
    def batch_mask(self, data_list: List[Dict[str, any]], 
                   field_configs: Dict[str, tuple]) -> List[Dict[str, any]]:
        """
        批量脱敏
        
        Args:
            data_list: 数据列表
            field_configs: 字段配置 {字段名: (数据类型, 配置)}
            
        Returns:
            脱敏后的数据列表
        """
        if not isinstance(data_list, list):
            raise ValueError("data_list必须是列表")
        
        if not isinstance(field_configs, dict):
            raise ValueError("field_configs必须是字典")
        
        try:
            result = []
            for item in data_list:
                if not isinstance(item, dict):
                    raise ValueError("data_list中的每个元素必须是字典")
                
                masked_item = item.copy()
                for field, (data_type, config) in field_configs.items():
                    if field in masked_item:
                        masked_item[field] = self.mask(masked_item[field], data_type, config)
                result.append(masked_item)
            return result
        except Exception as e:
            raise RuntimeError(f"批量脱敏失败: {str(e)}")
    
    def _mask_string(self, data: str, data_type: Optional[str], 
                     config: MaskingConfig) -> str:
        """内部字符串脱敏方法"""
        if data_type == 'email':
            return self.mask_email(data, config)
        elif data_type == 'phone':
            return self.mask_phone(data, config)
        elif data_type == 'credit_card':
            return self.mask_credit_card(data, config)
        elif data_type == 'id_card':
            return self.mask_id_card(data, config)
        elif data_type == 'name':
            return self.mask_name(data, config)
        elif data_type == 'ip':
            return self.mask_ip(data, config)
        else:
            # 默认部分脱敏
            if len(data) <= config.keep_prefix + config.keep_suffix:
                return config.mask_char * len(data)
            return (data[:config.keep_prefix] + 
                   config.mask_char * (len(data) - config.keep_prefix - config.keep_suffix) + 
                   data[-config.keep_suffix:])
    
    def _mask_dict(self, data: Dict, config: MaskingConfig) -> Dict:
        """递归脱敏字典"""
        result = {}
        for key, value in data.items():
            if isinstance(value, (dict, list, str)):
                result[key] = self.mask(value, config=config)
            else:
                result[key] = value
        return result
    
    def _mask_list(self, data: List, config: MaskingConfig) -> List:
        """递归脱敏列表"""
        return [self.mask(item, config=config) for item in data]
    
    def _hash_data(self, data: str, config: MaskingConfig) -> str:
        """哈希脱敏"""
        hash_func = getattr(hashlib, config.hash_algorithm, hashlib.sha256)
        return hash_func(data.encode()).hexdigest()
    
    def _tokenize(self, data: str) -> str:
        """令牌化脱敏"""
        if data not in self._token_map:
            self._token_map[data] = f"TOKEN_{secrets.token_hex(8)}"
        return self._token_map[data]
    
    def get_token_map(self) -> Dict[str, str]:
        """获取令牌映射表"""
        return self._token_map.copy()
    
    def clear_token_map(self):
        """清空令牌映射表"""
        self._token_map.clear()


# 使用示例
if __name__ == "__main__":
    masker = DataMaskerV2()
    
    # 邮箱脱敏
    print(masker.mask_email("user@example.com"))
    
    # 手机号脱敏
    print(masker.mask_phone("13812345678"))
    
    # 信用卡脱敏
    print(masker.mask_credit_card("1234567890123456"))
    
    # 身份证脱敏
    print(masker.mask_id_card("110101199001011234"))
    
    # 姓名脱敏
    print(masker.mask_name("张三"))
    
    # IP脱敏
    print(masker.mask_ip("192.168.1.1"))
    
    # 批量脱敏
    data = [
        {"name": "张三", "email": "zhangsan@example.com", "phone": "13812345678"},
        {"name": "李四", "email": "lisi@example.com", "phone": "13987654321"}
    ]
    
    field_configs = {
        "name": ("name", MaskingConfig(strategy=MaskingStrategy.PARTIAL)),
        "email": ("email", MaskingConfig(strategy=MaskingStrategy.PARTIAL)),
        "phone": ("phone", MaskingConfig(strategy=MaskingStrategy.PARTIAL))
    }
    
    masked_data = masker.batch_mask(data, field_configs)
    print(masked_data)