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
            env_file: .env文件路径，默认为当前目录的.env
            env_dir: .env文件所在目录，默认为当前目录
        """
        self.env_dir = Path(env_dir) if env_dir else Path.cwd()
        self.env_file = env_file or '.env'
        self._loaded = False
        self._cache: Dict[str, Any] = {}
    
    def load(self, override: bool = False) -> 'EnvLoader':
        """
        加载环境变量
        
        Args:
            override: 是否覆盖已存在的环境变量
        
        Returns:
            self，支持链式调用
        """
        env_path = self.env_dir / self.env_file
        
        if env_path.exists():
            load_dotenv(env_path, override=override)
            self._loaded = True
        
        # 加载环境特定的配置文件
        env = os.getenv('ENV', os.getenv('ENVIRONMENT', 'development'))
        env_specific_file = self.env_dir / f'.env.{env}'
        
        if env_specific_file.exists():
            load_dotenv(env_specific_file, override=True)
        
        # 加载本地配置（优先级最高）
        local_env_file = self.env_dir / '.env.local'
        if local_env_file.exists():
            load_dotenv(local_env_file, override=True)
        
        return self
    
    def get(self, key: str, default: Any = None, required: bool = False) -> Any:
        """
        获取环境变量
        
        Args:
            key: 环境变量名
            default: 默认值
            required: 是否必需
        
        Returns:
            环境变量值
        
        Raises:
            ValueError: 当required=True且变量不存在时
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
            return default
    
    def get_float(self, key: str, default: float = 0.0, required: bool = False) -> float:
        """获取浮点数类型环境变量"""
        value = self.get(key, default, required)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
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
        value = self.get(key, None, required)
        if value is None:
            return default or []
        if isinstance(value, list):
            return value
        return [item.strip() for item in str(value).split(separator) if item.strip()]
    
    def get_dict(self, key: str, default: Optional[Dict[str, str]] = None,
                 item_separator: str = ',', kv_separator: str = '=',
                 required: bool = False) -> Dict[str, str]:
        """获取字典类型环境变量"""
        value = self.get(key, None, required)
        if value is None:
            return default or {}
        if isinstance(value, dict):
            return value
        
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
    
    def clear_cache(self) -> None:
        """清空缓存"""
        self._cache.clear()
    
    def is_loaded(self) -> bool:
        """检查是否已加载"""
        return self._loaded
    
    def get_all(self) -> Dict[str, str]:
        """获取所有环境变量"""
        return dict(os.environ)
    
    def __getitem__(self, key: str) -> Any:
        """支持字典式访问"""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """支持字典式设置"""
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        """支持in操作符"""
        return key in os.environ


# 使用示例
if __name__ == '__main__':
    # 创建加载器并加载环境变量
    env = EnvLoader().load()
    
    # 获取不同类型的环境变量
    db_host = env.get_str('DB_HOST', 'localhost')
    db_port = env.get_int('DB_PORT', 5432)
    debug_mode = env.get_bool('DEBUG', False)
    allowed_hosts = env.get_list('ALLOWED_HOSTS', ['localhost'])
    
    # 必需的环境变量
    try:
        api_key = env.get('API_KEY', required=True)
    except ValueError as e:
        print(f"Error: {e}")
    
    # 字典式访问
    app_name = env['APP_NAME'] if 'APP_NAME' in env else 'MyApp'
    
    print(f"DB: {db_host}:{db_port}")
    print(f"Debug: {debug_mode}")
    print(f"Hosts: {allowed_hosts}")