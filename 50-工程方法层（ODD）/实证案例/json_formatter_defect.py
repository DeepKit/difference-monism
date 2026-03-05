import json
from typing import Any, Optional


class JSONFormatter:
    def __init__(self, indent: int = 2, ensure_ascii: bool = False):
        self.indent = indent
        self.ensure_ascii = ensure_ascii
    
    def format(self, data: Any) -> str:
        """格式化JSON数据"""
        return json.dumps(data, indent=self.indent, ensure_ascii=self.ensure_ascii)
    
    def format_compact(self, data: Any) -> str:
        """紧凑格式"""
        return json.dumps(data, separators=(',', ':'), ensure_ascii=self.ensure_ascii)
    
    def parse(self, json_str: str) -> Any:
        """解析JSON字符串"""
        return json.loads(json_str)
    
    def format_file(self, data: Any, filepath: str) -> None:
        """格式化并写入文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=self.indent, ensure_ascii=self.ensure_ascii)


# 使用示例
if __name__ == '__main__':
    formatter = JSONFormatter()
    
    data = {'name': '张三', 'age': 25, 'items': [1, 2, 3]}
    
    # 格式化输出
    print(formatter.format(data))
    
    # 紧凑输出
    print(formatter.format_compact(data))