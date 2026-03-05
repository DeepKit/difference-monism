from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class LogAggregator:
    def __init__(self):
        self.logs: List[Dict] = []
        self.logs_by_level: Dict[LogLevel, List[Dict]] = defaultdict(list)
        self.logs_by_source: Dict[str, List[Dict]] = defaultdict(list)
    
    def add_log(self, message: str, level: LogLevel, source: str = "default"):
        """添加日志条目"""
        log_entry = {
            "timestamp": datetime.now(),
            "message": message,
            "level": level,
            "source": source
        }
        
        self.logs.append(log_entry)
        self.logs_by_level[level].append(log_entry)
        self.logs_by_source[source].append(log_entry)
    
    def get_logs(self, level: Optional[LogLevel] = None, 
                 source: Optional[str] = None) -> List[Dict]:
        """获取过滤后的日志"""
        if level and source:
            return [log for log in self.logs_by_level[level] 
                    if log["source"] == source]
        elif level:
            return self.logs_by_level[level]
        elif source:
            return self.logs_by_source[source]
        return self.logs
    
    def get_stats(self) -> Dict:
        """获取日志统计信息"""
        return {
            "total": len(self.logs),
            "by_level": {level.name: len(logs) 
                        for level, logs in self.logs_by_level.items()},
            "by_source": {source: len(logs) 
                         for source, logs in self.logs_by_source.items()}
        }
    
    def clear(self):
        """清空所有日志"""
        self.logs.clear()
        self.logs_by_level.clear()
        self.logs_by_source.clear()


# 使用示例
if __name__ == "__main__":
    aggregator = LogAggregator()
    
    aggregator.add_log("应用启动", LogLevel.INFO, "app")
    aggregator.add_log("数据库连接失败", LogLevel.ERROR, "database")
    aggregator.add_log("调试信息", LogLevel.DEBUG, "app")
    
    print("所有日志:", len(aggregator.get_logs()))
    print("错误日志:", len(aggregator.get_logs(level=LogLevel.ERROR)))
    print("统计:", aggregator.get_stats())