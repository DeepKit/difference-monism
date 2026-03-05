import os
from pathlib import Path
from typing import Any, Optional, Union, Dict, List
from dotenv import load_dotenv


class EnvLoader:
    """环境变量加载器"""
    
    def __init__(self, env_file: Optional[str] = None, env_dir: Optional[str] = None):
        """
        初始化环境变量加载器
        
        Args:
            env_file: .env 文件路径
            env_dir: .env 文件所在目录
        """
        self.env_dir = Path(env_dir) if env_dir else Path.cwd()
        self.env_file = env_file
        self._loaded = False
        self._cache: Dict[str, Any] = {}
        
    def load(self, override: bool = False) -> 'EnvLoader':
        """
        加载环境变量
        
        Args:
            override: 是否覆盖已存在的环境变量
            
        Returns:
            self
        """
        if self._loaded and not override:
            return self
            
        # 加载基础 .env 文件
        base_env = self.env_dir / '.env'
        if base_env.exists():
            load_dotenv(base_env, override=override)
        
        # 加载环境特定文件
        env = os.getenv('ENV', os.getenv('ENVIRONMENT', 'development'))
        env_specific = self.env_dir / f'.env.{env}'
        if env_specific.exists():
            load_dotenv(env_specific, override=True)
        
        # 加载本地覆盖文件
        local_env = self.env_dir / '.env.local'
        if local_env.exists():
            load_dotenv(local_env, override=True)
        
        # 加载自定义文件
        if self.env_file:
            custom_path = Path(self.env_file)
            if custom_path.exists():
                load_dotenv(custom_path, override=True)
        
        self._loaded = True
        return self
    
    def get(self, key: str, default: Any = None, required: bool = False) -> Any:
        """
        获取环境变量
        
        Args:
            key: 变量名
            default: 默认值
            required: 是否必需
            
        Returns:
            环境变量值
        """
        if key in self._cache:
            return self._cache[key]
            
        value = os.getenv(key, default)
        
        if required and value is None:
            raise ValueError(f"Required environment variable '{key}' is not set")
        
        self._cache[key] = value
        return value
    
    def get_str(self, key: str, default: str = '', required: bool = False) -> str:
        """获取字符串类型环境变量"""
        value = self.get(key, default, required)
        return str(value) if value is not None else default
    
    def get_int(self, key: str, default: int = 0, required: bool = False) -> int:
        """获取整数类型环境变量"""
        value = self.get(key, default, required)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            if required:
                raise ValueError(f"Environment variable '{key}' must be an integer")
            return default
    
    def get_float(self, key: str, default: float = 0.0, required: bool = False) -> float:
        """获取浮点数类型环境变量"""
        value = self.get(key, default, required)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            if required:
                raise ValueError(f"Environment variable '{key}' must be a float")
            return default
    
    def get_bool(self, key: str, default: bool = False, required: bool = False) -> bool:
        """获取布尔类型环境变量"""
        value = self.get(key, default, required)
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        return str(value).lower() in ('true', '1', 'yes', 'on', 't', 'y')
    
    def get_list(self, key: str, default: Optional[List[str]] = None, 
                 separator: str = ',', required: bool = False) -> List[str]:
        """获取列表类型环境变量"""
        if default is None:
            default = []
        value = self.get(key, None, required)
        if value is None:
            return default
        return [item.strip() for item in str(value).split(separator) if item.strip()]
    
    def get_dict(self, key: str, default: Optional[Dict[str, str]] = None,
                 item_separator: str = ',', kv_separator: str = '=',
                 required: bool = False) -> Dict[str, str]:
        """获取字典类型环境变量"""
        if default is None:
            default = {}
        value = self.get(key, None, required)
        if value is None:
            return default
        
        result = {}
        items = str(value).split(item_separator)
        for item in items:
            if kv_separator in item:
                k, v = item.split(kv_separator, 1)
                result[k.strip()] = v.strip()
        return result
    
    def set(self, key: str, value: Any) -> None:
        """设置环境变量"""
        os.environ[key] = str(value)
        self._cache[key] = value
    
    def has(self, key: str) -> bool:
        """检查环境变量是否存在"""
        return key in os.environ
    
    def clear_cache(self) -> None:
        """清除缓存"""
        self._cache.clear()
    
    def reload(self) -> 'EnvLoader':
        """重新加载环境变量"""
        self.clear_cache()
        self._loaded = False
        return self.load(override=True)
    
    def to_dict(self) -> Dict[str, str]:
        """导出所有环境变量为字典"""
        return dict(os.environ)
    
    def validate(self, schema: Dict[str, Dict[str, Any]]) -> None:
        """
        验证环境变量
        
        Args:
            schema: 验证模式，格式如:
                {
                    'VAR_NAME': {
                        'type': 'str',  # str, int, float, bool, list
                        'required': True,
                        'default': 'value',
                        'choices': ['opt1', 'opt2']
                    }
                }
        """
        for key, rules in schema.items():
            required = rules.get('required', False)
            var_type = rules.get('type', 'str')
            default = rules.get('default')
            choices = rules.get('choices')
            
            # 获取值
            if var_type == 'int':
                value = self.get_int(key, default, required)
            elif var_type == 'float':
                value = self.get_float(key, default, required)
            elif var_type == 'bool':
                value = self.get_bool(key, default, required)
            elif var_type == 'list':
                value = self.get_list(key, default, required=required)
            else:
                value = self.get_str(key, default, required)
            
            # 验证选项
            if choices and value not in choices:
                raise ValueError(
                    f"Environment variable '{key}' must be one of {choices}, got '{value}'"
                )


# 使用示例
if __name__ == '__main__':
    # 创建加载器
    env = EnvLoader()
    env.load()
    
    # 获取各种类型的环境变量
    db_host = env.get_str('DB_HOST', 'localhost')
    db_port = env.get_int('DB_PORT', 5432)
    debug = env.get_bool('DEBUG', False)
    allowed_hosts = env.get_list('ALLOWED_HOSTS', ['localhost'])
    
    # 验证环境变量
    env.validate({
        'DB_HOST': {'type': 'str', 'required': True},
        'DB_PORT': {'type': 'int', 'default': 5432},
        'DEBUG': {'type': 'bool', 'default': False},
        'ENV': {'type': 'str', 'choices': ['development', 'production', 'test']}
    })