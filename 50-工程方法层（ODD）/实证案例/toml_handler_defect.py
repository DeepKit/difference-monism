"""
TOML处理类 - 完整实现
支持读取、写入、解析和操作TOML文件
"""

import tomli
import tomli_w
from pathlib import Path
from typing import Any, Dict, Optional, Union


class TOMLHandler:
    """TOML文件处理类"""
    
    def __init__(self, file_path: Optional[Union[str, Path]] = None):
        """
        初始化TOML处理器
        
        Args:
            file_path: TOML文件路径（可选）
        """
        self.file_path = Path(file_path) if file_path else None
        self.data: Dict[str, Any] = {}
    
    def load(self, file_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """
        从文件加载TOML数据
        
        Args:
            file_path: TOML文件路径，如果为None则使用初始化时的路径
            
        Returns:
            解析后的字典数据
        """
        path = Path(file_path) if file_path else self.file_path
        if not path:
            raise ValueError("未指定文件路径")
        
        with open(path, "rb") as f:
            self.data = tomli.load(f)
        return self.data
    
    def loads(self, toml_string: str) -> Dict[str, Any]:
        """
        从字符串解析TOML数据
        
        Args:
            toml_string: TOML格式字符串
            
        Returns:
            解析后的字典数据
        """
        self.data = tomli.loads(toml_string)
        return self.data
    
    def save(self, file_path: Optional[Union[str, Path]] = None, 
             data: Optional[Dict[str, Any]] = None) -> None:
        """
        保存TOML数据到文件
        
        Args:
            file_path: 保存路径，如果为None则使用初始化时的路径
            data: 要保存的数据，如果为None则使用当前data
        """
        path = Path(file_path) if file_path else self.file_path
        if not path:
            raise ValueError("未指定文件路径")
        
        save_data = data if data is not None else self.data
        
        with open(path, "wb") as f:
            tomli_w.dump(save_data, f)
    
    def dumps(self, data: Optional[Dict[str, Any]] = None) -> str:
        """
        将数据转换为TOML字符串
        
        Args:
            data: 要转换的数据，如果为None则使用当前data
            
        Returns:
            TOML格式字符串
        """
        dump_data = data if data is not None else self.data
        return tomli_w.dumps(dump_data)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取指定键的值，支持点号分隔的嵌套键
        
        Args:
            key: 键名，支持 "section.subsection.key" 格式
            default: 默认值
            
        Returns:
            键对应的值
        """
        keys = key.split(".")
        value = self.data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        设置指定键的值，支持点号分隔的嵌套键
        
        Args:
            key: 键名，支持 "section.subsection.key" 格式
            value: 要设置的值
        """
        keys = key.split(".")
        data = self.data
        
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        
        data[keys[-1]] = value
    
    def delete(self, key: str) -> bool:
        """
        删除指定键
        
        Args:
            key: 键名，支持 "section.subsection.key" 格式
            
        Returns:
            是否成功删除
        """
        keys = key.split(".")
        data = self.data
        
        for k in keys[:-1]:
            if k not in data:
                return False
            data = data[k]
        
        if keys[-1] in data:
            del data[keys[-1]]
            return True
        return False
    
    def has(self, key: str) -> bool:
        """
        检查键是否存在
        
        Args:
            key: 键名，支持 "section.subsection.key" 格式
            
        Returns:
            键是否存在
        """
        return self.get(key, object()) is not object()
    
    def update(self, data: Dict[str, Any]) -> None:
        """
        更新数据（合并）
        
        Args:
            data: 要合并的数据
        """
        self._deep_update(self.data, data)
    
    def _deep_update(self, target: Dict, source: Dict) -> None:
        """递归深度更新字典"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def clear(self) -> None:
        """清空所有数据"""
        self.data = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """返回数据的副本"""
        return self.data.copy()
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """从字典加载数据"""
        self.data = data.copy()


# 使用示例
if __name__ == "__main__":
    # 创建处理器
    handler = TOMLHandler("config.toml")
    
    # 设置数据
    handler.set("database.host", "localhost")
    handler.set("database.port", 5432)
    handler.set("server.debug", True)
    
    # 保存到文件
    handler.save()
    
    # 加载文件
    handler.load()
    
    # 获取值
    host = handler.get("database.host")
    print(f"Host: {host}")
    
    # 转换为字符串
    toml_str = handler.dumps()
    print(toml_str)