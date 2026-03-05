import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Callable
import yaml


class ConfigError(Exception):
    pass


class ConfigLoadError(ConfigError):
    pass


class ConfigValidationError(ConfigError):
    pass


class ConfigManager:
    def __init__(self, config_path: Optional[str] = None, defaults: Optional[Dict[str, Any]] = None, env_prefix: str = "APP_", validators: Optional[Dict[str, Callable]] = None):
        self.config_path = config_path
        self.defaults = defaults or {}
        self.env_prefix = env_prefix
        self.validators = validators or {}
        self._config: Dict[str, Any] = {}
        if config_path:
            self.load()
    
    def load(self, config_path: Optional[str] = None) -> None:
        path = config_path or self.config_path
        if not path:
            raise ConfigLoadError("未指定配置文件路径")
        config_file = Path(path)
        if not config_file.exists():
            raise ConfigLoadError(f"配置文件不存在: {path}")
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.suffix.lower() in ['.json']:
                    loaded_config = json.load(f)
                elif config_file.suffix.lower() in ['.yaml', '.yml']:
                    loaded_config = yaml.safe_load(f)
                else:
                    raise ConfigLoadError(f"不支持的配置文件格式: {config_file.suffix}")
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"JSON解析错误: {str(e)}")
        except yaml.YAMLError as e:
            raise ConfigLoadError(f"YAML解析错误: {str(e)}")
        except Exception as e:
            raise ConfigLoadError(f"读取配置文件失败: {str(e)}")
        self._config = {**self.defaults, **loaded_config}
        self._apply_env_overrides()
        self.validate()
    
    def reload(self) -> None:
        if not self.config_path:
            raise ConfigLoadError("无法重载：未设置配置文件路径")
        self.load()
    
    def _apply_env_overrides(self) -> None:
        for key in self._config.keys():
            env_key = f"{self.env_prefix}{key.upper()}"
            env_value = os.environ.get(env_key)
            if env_value is not None:
                self._config[key] = self._convert_env_value(env_value, self._config[key])
    
    def _convert_env_value(self, env_value: str, original_value: Any) -> Any:
        if isinstance(original_value, bool):
            return env_value.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(original_value, int):
            try:
                return int(env_value)
            except ValueError:
                return env_value
        elif isinstance(original_value, float):
            try:
                return float(env_value)
            except ValueError:
                return env_value
        elif isinstance(original_value, list):
            return [item.strip() for item in env_value.split(',')]
        else:
            return env_value
    
    def validate(self) -> None:
        for key, validator in self.validators.items():
            if key not in self._config:
                raise ConfigValidationError(f"缺少必需的配置项: {key}")
            value = self._config[key]
            try:
                if not validator(value):
                    raise ConfigValidationError(f"配置项 '{key}' 验证失败: 值 '{value}' 不符合要求")
            except Exception as e:
                raise ConfigValidationError(f"配置项 '{key}' 验证时发生错误: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def get_all(self) -> Dict[str, Any]:
        return self._config.copy()
    
    def add_validator(self, key: str, validator: Callable) -> None:
        self.validators[key] = validator
