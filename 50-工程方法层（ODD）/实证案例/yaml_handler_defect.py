import yaml
from pathlib import Path
from typing import Any, Dict, List, Union, Optional
import json


class YAMLHandler:
    """YAML文件处理类"""
    
    def __init__(self, default_flow_style: bool = False, sort_keys: bool = False):
        """
        初始化YAML处理器
        
        Args:
            default_flow_style: 是否使用流式风格（紧凑格式）
            sort_keys: 是否对键进行排序
        """
        self.default_flow_style = default_flow_style
        self.sort_keys = sort_keys
    
    def read(self, file_path: Union[str, Path]) -> Any:
        """
        读取YAML文件
        
        Args:
            file_path: YAML文件路径
            
        Returns:
            解析后的数据
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"文件不存在: {file_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"YAML解析错误: {e}")
    
    def write(self, data: Any, file_path: Union[str, Path], 
              create_dirs: bool = True) -> None:
        """
        写入YAML文件
        
        Args:
            data: 要写入的数据
            file_path: 目标文件路径
            create_dirs: 是否自动创建目录
        """
        file_path = Path(file_path)
        
        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    data, 
                    f, 
                    default_flow_style=self.default_flow_style,
                    sort_keys=self.sort_keys,
                    allow_unicode=True,
                    indent=2
                )
        except Exception as e:
            raise IOError(f"写入文件失败: {e}")
    
    def loads(self, yaml_string: str) -> Any:
        """
        解析YAML字符串
        
        Args:
            yaml_string: YAML格式字符串
            
        Returns:
            解析后的数据
        """
        try:
            return yaml.safe_load(yaml_string)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML解析错误: {e}")
    
    def dumps(self, data: Any) -> str:
        """
        将数据转换为YAML字符串
        
        Args:
            data: 要转换的数据
            
        Returns:
            YAML格式字符串
        """
        try:
            return yaml.dump(
                data,
                default_flow_style=self.default_flow_style,
                sort_keys=self.sort_keys,
                allow_unicode=True,
                indent=2
            )
        except Exception as e:
            raise ValueError(f"数据转换失败: {e}")
    
    def merge(self, *file_paths: Union[str, Path]) -> Dict:
        """
        合并多个YAML文件
        
        Args:
            *file_paths: YAML文件路径列表
            
        Returns:
            合并后的字典
        """
        merged = {}
        for path in file_paths:
            data = self.read(path)
            if isinstance(data, dict):
                merged.update(data)
            else:
                raise ValueError(f"文件内容不是字典类型: {path}")
        return merged
    
    def update(self, file_path: Union[str, Path], updates: Dict) -> None:
        """
        更新YAML文件中的值
        
        Args:
            file_path: YAML文件路径
            updates: 要更新的键值对
        """
        data = self.read(file_path)
        if not isinstance(data, dict):
            raise ValueError("文件内容不是字典类型")
        
        data.update(updates)
        self.write(data, file_path)
    
    def get_value(self, file_path: Union[str, Path], 
                  key_path: str, default: Any = None) -> Any:
        """
        获取嵌套键的值
        
        Args:
            file_path: YAML文件路径
            key_path: 键路径，用点分隔（如 "server.port"）
            default: 默认值
            
        Returns:
            键对应的值
        """
        data = self.read(file_path)
        keys = key_path.split('.')
        
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default
        
        return data
    
    def set_value(self, file_path: Union[str, Path], 
                  key_path: str, value: Any) -> None:
        """
        设置嵌套键的值
        
        Args:
            file_path: YAML文件路径
            key_path: 键路径，用点分隔（如 "server.port"）
            value: 要设置的值
        """
        data = self.read(file_path)
        if not isinstance(data, dict):
            data = {}
        
        keys = key_path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        self.write(data, file_path)
    
    def validate(self, file_path: Union[str, Path]) -> bool:
        """
        验证YAML文件格式
        
        Args:
            file_path: YAML文件路径
            
        Returns:
            是否有效
        """
        try:
            self.read(file_path)
            return True
        except Exception:
            return False
    
    def to_json(self, file_path: Union[str, Path], 
                json_path: Optional[Union[str, Path]] = None) -> str:
        """
        将YAML转换为JSON
        
        Args:
            file_path: YAML文件路径
            json_path: JSON输出路径（可选）
            
        Returns:
            JSON字符串
        """
        data = self.read(file_path)
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        if json_path:
            Path(json_path).write_text(json_str, encoding='utf-8')
        
        return json_str
    
    def from_json(self, json_path: Union[str, Path], 
                  yaml_path: Union[str, Path]) -> None:
        """
        将JSON转换为YAML
        
        Args:
            json_path: JSON文件路径
            yaml_path: YAML输出路径
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.write(data, yaml_path)


# 使用示例
if __name__ == "__main__":
    handler = YAMLHandler()
    
    # 写入
    data = {
        "server": {
            "host": "localhost",
            "port": 8080
        },
        "database": {
            "url": "postgresql://localhost/db",
            "pool_size": 10
        }
    }
    handler.write(data, "config.yaml")
    
    # 读取
    config = handler.read("config.yaml")
    print(config)
    
    # 获取嵌套值
    port = handler.get_value("config.yaml", "server.port")
    print(f"Port: {port}")
    
    # 更新值
    handler.set_value("config.yaml", "server.port", 9000)