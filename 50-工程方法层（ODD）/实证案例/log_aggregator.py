import logging
import threading
import queue
import json
import re
from datetime import datetime
from typing import List, Dict, Optional, Callable, Any
from pathlib import Path
from enum import Enum
import traceback


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class LogEntry:
    """日志条目类"""
    def __init__(self, timestamp: datetime, level: LogLevel, source: str, 
                 message: str, metadata: Optional[Dict] = None):
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'level': self.level.name,
            'source': self.source,
            'message': self.message,
            'metadata': self.metadata
        }
    
    def __str__(self) -> str:
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] [{self.level.name}] [{self.source}] {self.message}"


class LogAggregator:
    """日志聚合器类"""
    
    def __init__(self, buffer_size: int = 1000, auto_flush_interval: int = 5):
        self.buffer_size = buffer_size
        self.auto_flush_interval = auto_flush_interval
        self.log_buffer = queue.Queue(maxsize=buffer_size)
        self.filters: List[Callable[[LogEntry], bool]] = []
        self.outputs: List[Callable[[LogEntry], None]] = []
        self.running = False
        self.lock = threading.Lock()
        self.worker_thread: Optional[threading.Thread] = None
        self.stats = {
            'total_logs': 0,
            'by_level': {level.name: 0 for level in LogLevel},
            'by_source': {},
            'errors': 0
        }
    
    def add_filter(self, filter_func: Callable[[LogEntry], bool]) -> None:
        """添加日志过滤器"""
        with self.lock:
            self.filters.append(filter_func)
    
    def add_output(self, output_func: Callable[[LogEntry], None]) -> None:
        """添加输出目标"""
        with self.lock:
            self.outputs.append(output_func)
    
    def add_file_output(self, filepath: str, format_json: bool = False) -> None:
        """添加文件输出"""
        def file_writer(entry: LogEntry):
            try:
                Path(filepath).parent.mkdir(parents=True, exist_ok=True)
                with open(filepath, 'a', encoding='utf-8') as f:
                    if format_json:
                        f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
                    else:
                        f.write(str(entry) + '\n')
            except Exception as e:
                self._handle_error(f"文件写入错误: {e}")
        
        self.add_output(file_writer)
    
    def add_console_output(self, colored: bool = True) -> None:
        """添加控制台输出"""
        colors = {
            'DEBUG': '\033[36m',
            'INFO': '\033[32m',
            'WARNING': '\033[33m',
            'ERROR': '\033[31m',
            'CRITICAL': '\033[35m',
            'RESET': '\033[0m'
        }
        
        def console_writer(entry: LogEntry):
            try:
                if colored:
                    color = colors.get(entry.level.name, colors['RESET'])
                    print(f"{color}{entry}{colors['RESET']}")
                else:
                    print(entry)
            except Exception as e:
                self._handle_error(f"控制台输出错误: {e}")
        
        self.add_output(console_writer)
    
    def add_level_filter(self, min_level: LogLevel) -> None:
        """添加日志级别过滤器"""
        self.add_filter(lambda entry: entry.level.value >= min_level.value)
    
    def add_source_filter(self, sources: List[str]) -> None:
        """添加来源过滤器"""
        self.add_filter(lambda entry: entry.source in sources)
    
    def add_pattern_filter(self, pattern: str) -> None:
        """添加正则表达式过滤器"""
        regex = re.compile(pattern)
        self.add_filter(lambda entry: regex.search(entry.message) is not None)
    
    def log(self, level: LogLevel, source: str, message: str, 
            metadata: Optional[Dict] = None) -> None:
        """添加日志条目"""
        try:
            entry = LogEntry(datetime.now(), level, source, message, metadata)
            
            # 应用过滤器
            if self.filters:
                if not all(f(entry) for f in self.filters):
                    return
            
            # 更新统计
            with self.lock:
                self.stats['total_logs'] += 1
                self.stats['by_level'][level.name] += 1
                self.stats['by_source'][source] = self.stats['by_source'].get(source, 0) + 1
            
            # 添加到缓冲区
            try:
                self.log_buffer.put(entry, block=False)
            except queue.Full:
                self._handle_error("日志缓冲区已满，丢弃日志")
                
        except Exception as e:
            self._handle_error(f"日志添加错误: {e}")
    
    def debug(self, source: str, message: str, metadata: Optional[Dict] = None) -> None:
        self.log(LogLevel.DEBUG, source, message, metadata)
    
    def info(self, source: str, message: str, metadata: Optional[Dict] = None) -> None:
        self.log(LogLevel.INFO, source, message, metadata)
    
    def warning(self, source: str, message: str, metadata: Optional[Dict] = None) -> None:
        self.log(LogLevel.WARNING, source, message, metadata)
    
    def error(self, source: str, message: str, metadata: Optional[Dict] = None) -> None:
        self.log(LogLevel.ERROR, source, message, metadata)
    
    def critical(self, source: str, message: str, metadata: Optional[Dict] = None) -> None:
        self.log(LogLevel.CRITICAL, source, message, metadata)
    
    def parse_log_line(self, line: str, source: str = "parsed") -> Optional[LogEntry]:
        """解析日志行"""
        try:
            # 尝试解析JSON格式
            if line.strip().startswith('{'):
                data = json.loads(line)
                return LogEntry(
                    timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
                    level=LogLevel[data.get('level', 'INFO')],
                    source=data.get('source', source),
                    message=data.get('message', ''),
                    metadata=data.get('metadata', {})
                )
            
            # 尝试解析标准格式 [timestamp] [level] [source] message
            pattern = r'\[([^\]]+)\]\s*\[([^\]]+)\]\s*\[([^\]]+)\]\s*(.+)'
            match = re.match(pattern, line)
            if match:
                timestamp_str, level_str, source_str, message = match.groups()
                return LogEntry(
                    timestamp=datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S'),
                    level=LogLevel[level_str],
                    source=source_str,
                    message=message,
                    metadata={}
                )
            
            # 默认处理
            return LogEntry(datetime.now(), LogLevel.INFO, source, line, {})
            
        except Exception as e:
            self._handle_error(f"日志解析错误: {e}")
            return None
    
    def ingest_from_file(self, filepath: str, source: Optional[str] = None) -> int:
        """从文件导入日志"""
        count = 0
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    entry = self.parse_log_line(line, source or Path(filepath).stem)
                    if entry:
                        self.log(entry.level, entry.source, entry.message, entry.metadata)
                        count += 1
        except FileNotFoundError:
            self._handle_error(f"文件未找到: {filepath}")
        except Exception as e:
            self._handle_error(f"文件读取错误: {e}")
        
        return count
    
    def start(self) -> None:
        """启动日志处理线程"""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_logs, daemon=True)
        self.worker_thread.start()
    
    def stop(self) -> None:
        """停止日志处理"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        self.flush()
    
    def _process_logs(self) -> None:
        """处理日志的工作线程"""
        while self.running:
            try:
                entry = self.log_buffer.get(timeout=self.auto_flush_interval)
                self._output_log(entry)
            except queue.Empty:
                continue
            except Exception as e:
                self._handle_error(f"日志处理错误: {e}")
    
    def _output_log(self, entry: LogEntry) -> None:
        """输出日志到所有目标"""
        for output in self.outputs:
            try:
                output(entry)
            except Exception as e:
                self._handle_error(f"日志输出错误: {e}")
    
    def flush(self) -> None:
        """刷新缓冲区"""
        while not self.log_buffer.empty():
            try:
                entry = self.log_buffer.get_nowait()
                self._output_log(entry)
            except queue.Empty:
                break
            except Exception as e:
                self._handle_error(f"刷新错误: {e}")
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self.lock:
            return self.stats.copy()
    
    def clear_stats(self) -> None:
        """清除统计信息"""
        with self.lock:
            self.stats = {
                'total_logs': 0,
                'by_level': {level.name: 0 for level in LogLevel},
                'by_source': {},
                'errors': 0
            }
    
    def _handle_error(self, error_msg: str) -> None:
        """处理内部错误"""
        with self.lock:
            self.stats['errors'] += 1
        print(f"[LogAggregator Error] {error_msg}", file=__import__('sys').stderr)
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


# 使用示例
if __name__ == "__main__":
    # 创建聚合器
    aggregator = LogAggregator(buffer_size=1000, auto_flush_interval=2)
    
    # 添加输出
    aggregator.add_console_output(colored=True)
    aggregator.add_file_output("logs/app.log", format_json=False)
    aggregator.add_file_output("logs/app.json", format_json=True)
    
    # 添加过滤器（只记录WARNING及以上级别）
    aggregator.add_level_filter(LogLevel.INFO)
    
    # 启动聚合器
    aggregator.start()
    
    # 记录日志
    aggregator.info("app", "应用启动")
    aggregator.debug("database", "连接数据库", {"host": "localhost", "port": 5432})
    aggregator.warning("api", "API响应缓慢", {"response_time": 2.5})
    aggregator.error("payment", "支付失败", {"order_id": "12345", "error": "超时"})
    aggregator.critical("system", "系统崩溃")
    
    # 从文件导入日志
    # aggregator.ingest_from_file("external.log", source="external")
    
    # 获取统计
    import time
    time.sleep(1)
    print("\n统计信息:", aggregator.get_stats())
    
    # 停止聚合器
    aggregator.stop()