import json
from typing import Any, Optional, Union


class JSONFormatter:
    """JSON格式化工具类"""
    
    def __init__(self, indent: int = 2, ensure_ascii: bool = False, 
                 sort_keys: bool = False):
        """
        初始化JSON格式化器
        
        Args:
            indent: 缩进空格数
            ensure_ascii: 是否转义非ASCII字符
            sort_keys: 是否排序键
        """
        self.indent = indent
        self.ensure_ascii = ensure_ascii
        self.sort_keys = sort_keys
    
    def format(self, data: Union[str, dict, list]) -> str:
        """
        格式化JSON数据
        
        Args:
            data: JSON字符串或Python对象
            
        Returns:
            格式化后的JSON字符串
        """
        if isinstance(data, str):
            data = json.loads(data)
        
        return json.dumps(
            data,
            indent=self.indent,
            ensure_ascii=self.ensure_ascii,
            sort_keys=self.sort_keys
        )
    
    def minify(self, data: Union[str, dict, list]) -> str:
        """
        压缩JSON（移除空格和换行）
        
        Args:
            data: JSON字符串或Python对象
            
        Returns:
            压缩后的JSON字符串
        """
        if isinstance(data, str):
            data = json.loads(data)
        
        return json.dumps(data, separators=(',', ':'), ensure_ascii=self.ensure_ascii)
    
    def validate(self, json_str: str) -> tuple[bool, Optional[str]]:
        """
        验证JSON格式
        
        Args:
            json_str: JSON字符串
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            json.loads(json_str)
            return True, None
        except json.JSONDecodeError as e:
            return False, str(e)
    
    def format_file(self, input_path: str, output_path: Optional[str] = None) -> None:
        """
        格式化JSON文件
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径（默认覆盖原文件）
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        formatted = self.format(data)
        
        output_path = output_path or input_path
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted)
    
    def to_dict(self, json_str: str) -> dict:
        """将JSON字符串转换为字典"""
        return json.loads(json_str)
    
    def from_dict(self, data: dict) -> str:
        """将字典转换为格式化的JSON字符串"""
        return self.format(data)


# 使用示例
if __name__ == "__main__":
    formatter = JSONFormatter(indent=4, sort_keys=True)
    
    # 示例数据
    data = {
        "name": "张三",
        "age": 30,
        "skills": ["Python", "JavaScript"],
        "address": {"city": "北京", "district": "朝阳区"}
    }
    
    # 格式化
    formatted = formatter.format(data)
    print("格式化输出:")
    print(formatted)
    
    # 压缩
    minified = formatter.minify(data)
    print("\n压缩输出:")
    print(minified)
    
    # 验证
    is_valid, error = formatter.validate(formatted)
    print(f"\n验证结果: {is_valid}")