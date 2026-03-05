from datetime import datetime
from zoneinfo import ZoneInfo


class TimezoneConverter:
    """时区转换工具类"""
    
    def __init__(self, default_timezone='UTC'):
        """
        初始化时区转换器
        
        Args:
            default_timezone: 默认时区，如 'UTC', 'Asia/Shanghai', 'America/New_York'
        """
        self.default_timezone = ZoneInfo(default_timezone)
    
    def convert(self, dt, from_tz, to_tz):
        """
        转换时区
        
        Args:
            dt: datetime对象（可以是naive或aware）
            from_tz: 源时区字符串
            to_tz: 目标时区字符串
            
        Returns:
            转换后的datetime对象
        """
        from_zone = ZoneInfo(from_tz)
        to_zone = ZoneInfo(to_tz)
        
        # 如果是naive datetime，先添加源时区信息
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=from_zone)
        
        # 转换到目标时区
        return dt.astimezone(to_zone)
    
    def now(self, timezone=None):
        """
        获取指定时区的当前时间
        
        Args:
            timezone: 时区字符串，None则使用默认时区
            
        Returns:
            当前时间的datetime对象
        """
        tz = ZoneInfo(timezone) if timezone else self.default_timezone
        return datetime.now(tz)
    
    def to_utc(self, dt, from_tz=None):
        """
        转换为UTC时间
        
        Args:
            dt: datetime对象
            from_tz: 源时区，None则使用默认时区
            
        Returns:
            UTC时间
        """
        if from_tz:
            from_zone = ZoneInfo(from_tz)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=from_zone)
        
        return dt.astimezone(ZoneInfo('UTC'))
    
    def from_utc(self, dt, to_tz):
        """
        从UTC转换到指定时区
        
        Args:
            dt: UTC时间的datetime对象
            to_tz: 目标时区字符串
            
        Returns:
            目标时区的datetime对象
        """
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo('UTC'))
        
        return dt.astimezone(ZoneInfo(to_tz))
    
    def format(self, dt, fmt='%Y-%m-%d %H:%M:%S %Z'):
        """
        格式化datetime对象
        
        Args:
            dt: datetime对象
            fmt: 格式字符串
            
        Returns:
            格式化后的字符串
        """
        return dt.strftime(fmt)
    
    @staticmethod
    def get_timezone_offset(timezone, dt=None):
        """
        获取时区偏移量
        
        Args:
            timezone: 时区字符串
            dt: datetime对象，None则使用当前时间
            
        Returns:
            偏移量字符串，如 '+08:00'
        """
        tz = ZoneInfo(timezone)
        if dt is None:
            dt = datetime.now(tz)
        elif dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz)
        
        offset = dt.strftime('%z')
        return f"{offset[:3]}:{offset[3:]}"


# 使用示例
if __name__ == '__main__':
    converter = TimezoneConverter('Asia/Shanghai')
    
    # 获取当前时间
    print("上海当前时间:", converter.now())
    print("纽约当前时间:", converter.now('America/New_York'))
    
    # 时区转换
    shanghai_time = datetime(2024, 1, 1, 12, 0, 0)
    ny_time = converter.convert(shanghai_time, 'Asia/Shanghai', 'America/New_York')
    print(f"上海 {shanghai_time} -> 纽约 {ny_time}")
    
    # 转换为UTC
    utc_time = converter.to_utc(shanghai_time, 'Asia/Shanghai')
    print(f"UTC时间: {utc_time}")
    
    # 获取时区偏移
    print("上海时区偏移:", converter.get_timezone_offset('Asia/Shanghai'))
    print("纽约时区偏移:", converter.get_timezone_offset('America/New_York'))