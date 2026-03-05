from datetime import datetime
from typing import Optional, List
import re


class DateParser:
    """日期解析类，支持多种常见日期格式"""
    
    DEFAULT_FORMATS = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%Y.%m.%d',
        '%Y%m%d',
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%d.%m.%Y',
        '%m-%d-%Y',
        '%m/%d/%Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y/%m/%d %H:%M',
        '%d-%m-%Y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%Y年%m月%d日',
        '%Y年%m月%d日 %H:%M:%S',
        '%Y年%m月%d日 %H时%M分%S秒',
        '%m月%d日',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S.%fZ',
    ]
    
    def __init__(self, formats: Optional[List[str]] = None):
        """
        初始化日期解析器
        
        Args:
            formats: 自定义日期格式列表，如果为None则使用默认格式
        """
        self.formats = formats if formats else self.DEFAULT_FORMATS
    
    def parse(self, date_string: str, fuzzy: bool = False) -> Optional[datetime]:
        """
        解析日期字符串
        
        Args:
            date_string: 日期字符串
            fuzzy: 是否启用模糊匹配（提取字符串中的日期部分）
            
        Returns:
            datetime对象，解析失败返回None
        """
        if not date_string or not isinstance(date_string, str):
            return None
        
        date_string = date_string.strip()
        
        # 尝试使用预定义格式解析
        for fmt in self.formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        # 模糊匹配模式
        if fuzzy:
            return self._fuzzy_parse(date_string)
        
        return None
    
    def _fuzzy_parse(self, date_string: str) -> Optional[datetime]:
        """模糊解析日期字符串"""
        # 匹配常见日期模式
        patterns = [
            (r'(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2})', '%Y-%m-%d %H:%M:%S'),
            (r'(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2})', '%Y-%m-%d %H:%M'),
            (r'(\d{4})-(\d{1,2})-(\d{1,2})', '%Y-%m-%d'),
            (r'(\d{4})/(\d{1,2})/(\d{1,2})', '%Y/%m/%d'),
            (r'(\d{4})年(\d{1,2})月(\d{1,2})日', '%Y年%m月%d日'),
        ]
        
        for pattern, fmt in patterns:
            match = re.search(pattern, date_string)
            if match:
                try:
                    matched_str = match.group(0)
                    return datetime.strptime(matched_str, fmt)
                except ValueError:
                    continue
        
        return None
    
    def parse_multiple(self, date_strings: List[str]) -> List[Optional[datetime]]:
        """
        批量解析日期字符串
        
        Args:
            date_strings: 日期字符串列表
            
        Returns:
            datetime对象列表
        """
        return [self.parse(ds) for ds in date_strings]
    
    def add_format(self, format_string: str):
        """添加自定义日期格式"""
        if format_string not in self.formats:
            self.formats.insert(0, format_string)
    
    def is_valid(self, date_string: str) -> bool:
        """检查日期字符串是否有效"""
        return self.parse(date_string) is not None
    
    @staticmethod
    def to_string(dt: datetime, format_string: str = '%Y-%m-%d') -> str:
        """
        将datetime对象转换为字符串
        
        Args:
            dt: datetime对象
            format_string: 输出格式
            
        Returns:
            格式化的日期字符串
        """
        return dt.strftime(format_string)


# 使用示例
if __name__ == '__main__':
    parser = DateParser()
    
    # 测试各种格式
    test_dates = [
        '2024-01-15',
        '2024/01/15',
        '15-01-2024',
        '2024年01月15日',
        '2024-01-15 14:30:00',
        '20240115',
        'Today is 2024-01-15 and tomorrow',
    ]
    
    for date_str in test_dates:
        result = parser.parse(date_str)
        fuzzy_result = parser.parse(date_str, fuzzy=True)
        print(f'{date_str:40} -> {result} (fuzzy: {fuzzy_result})')