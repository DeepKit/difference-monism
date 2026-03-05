
import threading
import time
from datetime import datetime, timedelta
from typing import Callable, Optional, Dict, List, Any
import re


class CronExpression:
    """Cron表达式解析器 (分 时 日 月 周)"""
    
    def __init__(self, expression: str):
        self.expression = expression
        parts = expression.split()
        if len(parts) != 5:
            raise ValueError("Cron表达式必须包含5个字段: 分 时 日 月 周")
        
        self.minute = self._parse_field(parts[0], 0, 59)
        self.hour = self._parse_field(parts[1], 0, 23)
        self.day = self._parse_field(parts[2], 1, 31)
        self.month = self._