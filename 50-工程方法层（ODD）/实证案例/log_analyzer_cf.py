import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from collections import Counter
from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEntry:
    def __init__(self, timestamp: datetime, level: str, message: str, raw_line: str):
        self.timestamp = timestamp
        self.level = level.upper()
        self.message = message
        self.raw_line = raw_line

    def __repr__(self):
        return f"LogEntry({self.timestamp}, {self.level}, {self.message[:50]}...)"


class LogAnalyzer:
    LOG_PATTERNS = [
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(?P<level>\w+)\s+(?P<message>.*)',
        r'\[(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s+(?P<level>\w+):\s+(?P<message>.*)',
        r'(?P<level>\w+)\s+(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+-\s+(?P<message>.*)',
        r'(?P<timestamp>\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})\s+\[(?P<level>\w+)\]\s+(?P<message>.*)',
    ]
    
    TIMESTAMP_FORMATS = ['%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']
    
    def __init__(self):
        self.logs: List[LogEntry] = []
        self.compiled_patterns = [re.compile(pattern) for pattern in self.LOG_PATTERNS]
    
    def parse_log_file(self, file_path: str) -> Tuple[bool, str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            parsed_count = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                log_entry = self._parse_log_line(line)
                if log_entry:
                    self.logs.append(log_entry)
                    parsed_count += 1
            if parsed_count == 0:
                return False, "未能解析任何日志条目，请检查日志格式"
            return True, f"成功解析 {parsed_count} 条日志"
        except FileNotFoundError:
            return False, f"文件不存在: {file_path}"
        except PermissionError:
            return False, f"没有权限读取文件: {file_path}"
        except Exception as e:
            return False, f"解析日志文件时出错: {str(e)}"
    
    def parse_log_lines(self, lines: List[str]) -> Tuple[bool, str]:
        try:
            parsed_count = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                log_entry = self._parse_log_line(line)
                if log_entry:
                    self.logs.append(log_entry)
                    parsed_count += 1
            if parsed_count == 0:
                return False, "未能解析任何日志条目，请检查日志格式"
            return True, f"成功解析 {parsed_count} 条日志"
        except Exception as e:
            return False, f"解析日志时出错: {str(e)}"
    
    def _parse_log_line(self, line: str) -> Optional[LogEntry]:
        for pattern in self.compiled_patterns:
            match = pattern.match(line)
            if match:
                try:
                    groups = match.groupdict()
                    timestamp_str = groups['timestamp']
                    level = groups['level']
                    message = groups['message']
                    timestamp = self._parse_timestamp(timestamp_str)
                    if timestamp:
                        return LogEntry(timestamp, level, message, line)
                except Exception:
                    continue
        return None
    
    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        for fmt in self.TIMESTAMP_FORMATS:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        return None
    
    def filter_by_level(self, levels: List[str]) -> List[LogEntry]:
        if not levels:
            return self.logs
        levels_upper = [level.upper() for level in levels]
        return [log for log in self.logs if log.level in levels_upper]
    
    def filter_by_time_range(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> List[LogEntry]:
        filtered = self.logs
        if start_time:
            filtered = [log for log in filtered if log.timestamp >= start_time]
        if end_time:
            filtered = [log for log in filtered if log.timestamp <= end_time]
        return filtered
    
    def search_by_keyword(self, keyword: str, case_sensitive: bool = False) -> List[LogEntry]:
        if not keyword:
            return self.logs
        if case_sensitive:
            return [log for log in self.logs if keyword in log.message]
        else:
            keyword_lower = keyword.lower()
            return [log for log in self.logs if keyword_lower in log.message.lower()]
    
    def get_level_statistics(self) -> Dict[str, int]:
        return dict(Counter(log.level for log in self.logs))
    
    def filter_logs(self, levels: Optional[List[str]] = None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, keyword: Optional[str] = None, case_sensitive: bool = False) -> List[LogEntry]:
        result = self.logs
        if levels:
            levels_upper = [level.upper() for level in levels]
            result = [log for log in result if log.level in levels_upper]
        if start_time:
            result = [log for log in result if log.timestamp >= start_time]
        if end_time:
            result = [log for log in result if log.timestamp <= end_time]
        if keyword:
            if case_sensitive:
                result = [log for log in result if keyword in log.message]
            else:
                keyword_lower = keyword.lower()
                result = [log for log in result if keyword_lower in log.message.lower()]
        return result
    
    def get_summary(self) -> Dict:
        if not self.logs:
            return {'total': 0, 'level_stats': {}, 'time_range': None}
        timestamps = [log.timestamp for log in self.logs]
        return {'total': len(self.logs), 'level_stats': self.get_level_statistics(), 'time_range': {'start': min(timestamps), 'end': max(timestamps)}}
    
    def clear(self):
        self.logs.clear()
