
from typing import List, Dict, Set
from datetime import datetime


class BusinessMetricsCalculator:
    def __init__(self):
        self.page_views: List[Dict] = []
        self.conversions: List[Dict] = []
    
    def add_page_view(self, user_id: str, page: str, timestamp: datetime = None):
        """添加页面浏览记录"""
        self.page_views.append({
            'user_id': user_id,
            'page': page,
            'timestamp': timestamp or datetime.now()
        })
    
    def add_conversion(self, user_id: str, conversion_type: str, timestamp: datetime = None):
        """添加转化记录"""
        self.conversions.append({
            'user_id': user_id,
            'conversion_type': conversion_type,
            'timestamp': timestamp or datetime.now()
        })
    
    def calculate_pv(self, page: str = None) -> int:
        """计算PV（页面浏览量）"""
        if page:
            return sum(1 for pv in self.page_views if pv['page'] == page)
        return len(self.page_views)
    
    def calculate_uv(self, page: str = None) -> int:
        """计算UV（独立访客数）"""
        if page:
            unique_users = {pv['user_id'] for pv in self.page_views if pv['page'] == page}
        else:
            unique_users = {pv['user_id'] for pv in self.page_views}
        return len(unique_users)
    
    def calculate_conversion_rate(self, conversion_type: str = None) -> float:
        """计算转化率"""
        uv = self.calculate_uv()
        if uv == 0:
            return 0.0
        
        if conversion_type:
            conversion_count = sum(1 for c in self.conversions if c['conversion_type'] == conversion_type)
        else:
            conversion_count = len(self.conversions)
        
        return (conversion_count / uv) * 100
    
    def get_metrics_summary(self) -> Dict:
        """获取指标汇总"""
        return {
            'pv': self.calculate_pv(),
            'uv': self.calculate_uv(),
            'conversion_rate': self.calculate_conversion_rate(),
            'pv_uv_ratio': self.calculate_pv() / self.calculate_uv() if self.calculate_uv() > 0 else 0
        }
    
    def reset(self):
        """重置所有数据"""
        self.page_views.clear()
        self.conversions.clear()


# 使用示例
if __name__ == "__main__":
    calculator = BusinessMetricsCalculator()
    
    # 添加页面浏览记录
    calculator.add_page_view("user1", "/home")
    calculator.add_page_view("user1", "/product")
    calculator.add_page_view("user2", "/home")
    calculator.add_page_view("user3", "/product")
    calculator.add_page_view("user1", "/checkout")
    
    # 添加转化记录
    calculator.add_conversion("user1", "purchase")
    calculator.add_conversion("user3", "signup")
    
    # 计算指标
    print(f"PV: {calculator.calculate_pv()}")
    print(f"UV: {calculator.calculate_uv()}")
    print(f"转化率: {calculator.calculate_conversion_rate():.2f}%")
    print(f"指标汇总: {calculator.get_metrics_summary()}")
