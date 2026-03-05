from datetime import datetime
from zoneinfo import ZoneInfo

class TimezoneConverter:
    def __init__(self, source_tz: str):
        """初始化转换器
        
        Args:
            source_tz: 源时区，如 'Asia/Shanghai', 'UTC'
        """
        self.source_tz = ZoneInfo(source_tz)
    
    def convert(self, dt: datetime, target_tz: str) -> datetime:
        """转换时区
        
        Args:
            dt: 待转换的datetime对象
            target_tz: 目标时区
            
        Returns:
            转换后的datetime对象
        """
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=self.source_tz)
        return dt.astimezone(ZoneInfo(target_tz))
    
    def now_in(self, target_tz: str) -> datetime:
        """获取指定时区的当前时间"""
        return datetime.now(ZoneInfo(target_tz))
    
    @staticmethod
    def convert_between(dt: datetime, from_tz: str, to_tz: str) -> datetime:
        """静态方法：在两个时区间转换"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo(from_tz))
        return dt.astimezone(ZoneInfo(to_tz))


# 使用示例
if __name__ == "__main__":
    # 创建转换器
    converter = TimezoneConverter('Asia/Shanghai')
    
    # 转换时间
    dt = datetime(2024, 1, 1, 12, 0, 0)
    ny_time = converter.convert(dt, 'America/New_York')
    print(f"上海 {dt} -> 纽约 {ny_time}")
    
    # 获取当前时间
    tokyo_now = converter.now_in('Asia/Tokyo')
    print(f"东京当前时间: {tokyo_now}")
    
    # 静态方法转换
    utc_time = TimezoneConverter.convert_between(
        datetime(2024, 1, 1, 12, 0, 0),
        'Asia/Shanghai',
        'UTC'
    )
    print(f"UTC时间: {utc_time}")