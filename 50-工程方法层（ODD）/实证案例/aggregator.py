from typing import List, Union, Callable, Any, Dict
from collections import defaultdict
from statistics import mean, median, stdev, variance
from functools import reduce


class Aggregator:
    """通用数据聚合器"""
    
    def __init__(self):
        self.data: List[Any] = []
        self.grouped_data: Dict[Any, List[Any]] = defaultdict(list)
    
    def add(self, value: Any) -> 'Aggregator':
        """添加单个数据点"""
        self.data.append(value)
        return self
    
    def add_many(self, values: List[Any]) -> 'Aggregator':
        """批量添加数据"""
        self.data.extend(values)
        return self
    
    def group_by(self, key_func: Callable) -> 'Aggregator':
        """按键函数分组"""
        self.grouped_data.clear()
        for item in self.data:
            key = key_func(item)
            self.grouped_data[key].append(item)
        return self
    
    def sum(self) -> Union[int, float]:
        """求和"""
        return sum(self.data)
    
    def count(self) -> int:
        """计数"""
        return len(self.data)
    
    def avg(self) -> float:
        """平均值"""
        return mean(self.data) if self.data else 0
    
    def min(self) -> Any:
        """最小值"""
        return min(self.data) if self.data else None
    
    def max(self) -> Any:
        """最大值"""
        return max(self.data) if self.data else None
    
    def median(self) -> float:
        """中位数"""
        return median(self.data) if self.data else 0
    
    def std(self) -> float:
        """标准差"""
        return stdev(self.data) if len(self.data) > 1 else 0
    
    def var(self) -> float:
        """方差"""
        return variance(self.data) if len(self.data) > 1 else 0
    
    def unique(self) -> List[Any]:
        """去重"""
        return list(set(self.data))
    
    def filter(self, predicate: Callable) -> 'Aggregator':
        """过滤数据"""
        self.data = [x for x in self.data if predicate(x)]
        return self
    
    def map(self, func: Callable) -> 'Aggregator':
        """映射转换"""
        self.data = [func(x) for x in self.data]
        return self
    
    def reduce(self, func: Callable, initial: Any = None) -> Any:
        """归约操作"""
        if initial is None:
            return reduce(func, self.data)
        return reduce(func, self.data, initial)
    
    def top_n(self, n: int, reverse: bool = True) -> List[Any]:
        """获取前N个元素"""
        return sorted(self.data, reverse=reverse)[:n]
    
    def percentile(self, p: float) -> float:
        """百分位数"""
        if not self.data:
            return 0
        sorted_data = sorted(self.data)
        k = (len(sorted_data) - 1) * p / 100
        f = int(k)
        c = f + 1
        if c >= len(sorted_data):
            return sorted_data[-1]
        return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])
    
    def aggregate(self, func: Callable) -> Any:
        """自定义聚合函数"""
        return func(self.data)
    
    def group_aggregate(self, agg_func: Callable) -> Dict[Any, Any]:
        """分组聚合"""
        return {key: agg_func(values) for key, values in self.grouped_data.items()}
    
    def reset(self) -> 'Aggregator':
        """重置数据"""
        self.data.clear()
        self.grouped_data.clear()
        return self
    
    def get_data(self) -> List[Any]:
        """获取原始数据"""
        return self.data.copy()
    
    def get_grouped_data(self) -> Dict[Any, List[Any]]:
        """获取分组数据"""
        return dict(self.grouped_data)
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __repr__(self) -> str:
        return f"Aggregator(count={len(self.data)})"


# 使用示例
if __name__ == "__main__":
    # 基础聚合
    agg = Aggregator()
    agg.add_many([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    print(f"总和: {agg.sum()}")
    print(f"平均值: {agg.avg()}")
    print(f"中位数: {agg.median()}")
    print(f"最小值: {agg.min()}")
    print(f"最大值: {agg.max()}")
    print(f"标准差: {agg.std():.2f}")
    
    # 链式操作
    result = (Aggregator()
              .add_many([1, 2, 3, 4, 5])
              .filter(lambda x: x > 2)
              .map(lambda x: x * 2)
              .sum())
    print(f"链式操作结果: {result}")
    
    # 分组聚合
    data = [
        {"category": "A", "value": 10},
        {"category": "B", "value": 20},
        {"category": "A", "value": 15},
        {"category": "B", "value": 25},
    ]
    
    agg2 = Aggregator()
    agg2.add_many(data)
    agg2.group_by(lambda x: x["category"])
    
    group_sums = agg2.group_aggregate(lambda items: sum(item["value"] for item in items))
    print(f"分组求和: {group_sums}")