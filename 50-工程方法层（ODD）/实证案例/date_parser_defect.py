from datetime import datetime
from typing import Optional, List


class DateParser:
    """简洁的日期解析类"""
    
    # 常见日期格式
    FORMATS = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%Y.%m.%d',
        '%Y%m%d',
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%d.%m.%Y',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d %H:%M',
        '%d-%m-%Y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%b %d, %Y',
        '%B %d, %Y',
        '%d %b %Y',
        '%d %B %Y',
    ]
    
    def __init__(self, custom_formats: Optional[List[str]] = None):
        """初始化解析器
        
        Args:
            custom_formats: 自定义格式列表，会优先尝试这些格式
        """
        self.formats = (custom_formats or []) + self.FORMATS
    
    def parse(self, date_string: str) -> Optional[datetime]:
        """解析日期字符串
        
        Args:
            date_string: 日期字符串
            
        Returns:
            datetime对象，解析失败返回None
        """
        date_string = date_string.strip()
        
        for fmt in self.formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        return None
    
    def parse_or_raise(self, date_string: str) -> datetime:
        """解析日期字符串，失败则抛出异常
        
        Args:
            date_string: 日期字符串
            
        Returns:
            datetime对象
            
        Raises:
            ValueError: 无法解析日期
        """
        result = self.parse(date_string)
        if result is None:
            raise ValueError(f"无法解析日期: {date_string}")
        return result


# 使用示例
if __name__ == '__main__':
    parser = DateParser()
    
    test_dates = [
        '2024-01-15',
        '2024/01/15',
        '15-01-2024',
        '2024-01-15 14:30:00',
        'Jan 15, 2024',
        '20240115',
    ]
    
    for date_str in test_dates:
        result = parser.parse(date_str)
        print(f"{date_str:25} -> {result}")