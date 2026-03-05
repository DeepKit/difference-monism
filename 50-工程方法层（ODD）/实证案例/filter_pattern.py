import re
from typing import List, Callable, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class FilterAction(Enum):
    ALLOW = "allow"
    BLOCK = "block"


@dataclass
class Message:
    content: str
    sender: str
    timestamp: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class MessageFilter:
    def __init__(self):
        self.keyword_blacklist: List[str] = []
        self.keyword_whitelist: List[str] = []
        self.pattern_blacklist: List[re.Pattern] = []
        self.sender_blacklist: List[str] = []
        self.sender_whitelist: List[str] = []
        self.min_length: Optional[int] = None
        self.max_length: Optional[int] = None
        self.custom_filters: List[Callable[[Message], bool]] = []
        self.case_sensitive: bool = False

    def add_keyword_blacklist(self, keywords: List[str]) -> None:
        self.keyword_blacklist.extend(keywords)

    def add_keyword_whitelist(self, keywords: List[str]) -> None:
        self.keyword_whitelist.extend(keywords)

    def add_pattern_blacklist(self, patterns: List[str]) -> None:
        self.pattern_blacklist.extend([re.compile(p) for p in patterns])

    def add_sender_blacklist(self, senders: List[str]) -> None:
        self.sender_blacklist.extend(senders)

    def add_sender_whitelist(self, senders: List[str]) -> None:
        self.sender_whitelist.extend(senders)

    def set_length_limits(self, min_length: Optional[int] = None, 
                         max_length: Optional[int] = None) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def add_custom_filter(self, filter_func: Callable[[Message], bool]) -> None:
        self.custom_filters.append(filter_func)

    def _check_keywords(self, content: str) -> FilterAction:
        text = content if self.case_sensitive else content.lower()
        
        # Check whitelist first
        if self.keyword_whitelist:
            for keyword in self.keyword_whitelist:
                check_keyword = keyword if self.case_sensitive else keyword.lower()
                if check_keyword in text:
                    return FilterAction.ALLOW
        
        # Check blacklist
        for keyword in self.keyword_blacklist:
            check_keyword = keyword if self.case_sensitive else keyword.lower()
            if check_keyword in text:
                return FilterAction.BLOCK
        
        return FilterAction.ALLOW

    def _check_patterns(self, content: str) -> FilterAction:
        for pattern in self.pattern_blacklist:
            if pattern.search(content):
                return FilterAction.BLOCK
        return FilterAction.ALLOW

    def _check_sender(self, sender: str) -> FilterAction:
        if self.sender_whitelist and sender not in self.sender_whitelist:
            return FilterAction.BLOCK
        
        if sender in self.sender_blacklist:
            return FilterAction.BLOCK
        
        return FilterAction.ALLOW

    def _check_length(self, content: str) -> FilterAction:
        length = len(content)
        
        if self.min_length is not None and length < self.min_length:
            return FilterAction.BLOCK
        
        if self.max_length is not None and length > self.max_length:
            return FilterAction.BLOCK
        
        return FilterAction.ALLOW

    def filter(self, message: Message) -> bool:
        """Returns True if message should be allowed, False if blocked"""
        
        # Check sender
        if self._check_sender(message.sender) == FilterAction.BLOCK:
            return False
        
        # Check length
        if self._check_length(message.content) == FilterAction.BLOCK:
            return False
        
        # Check keywords
        if self._check_keywords(message.content) == FilterAction.BLOCK:
            return False
        
        # Check patterns
        if self._check_patterns(message.content) == FilterAction.BLOCK:
            return False
        
        # Check custom filters
        for custom_filter in self.custom_filters:
            if not custom_filter(message):
                return False
        
        return True

    def filter_batch(self, messages: List[Message]) -> List[Message]:
        """Filter a batch of messages, returning only allowed ones"""
        return [msg for msg in messages if self.filter(msg)]


# 使用示例
if __name__ == "__main__":
    # 创建过滤器
    filter = MessageFilter()
    
    # 添加黑名单关键词
    filter.add_keyword_blacklist(["spam", "广告", "垃圾"])
    
    # 添加正则模式黑名单
    filter.add_pattern_blacklist([r"\d{11}", r"http://\S+"])
    
    # 设置长度限制
    filter.set_length_limits(min_length=5, max_length=500)
    
    # 添加发件人黑名单
    filter.add_sender_blacklist(["spammer@example.com"])
    
    # 添加自定义过滤器
    filter.add_custom_filter(lambda msg: "!" not in msg.content)
    
    # 测试消息
    messages = [
        Message("Hello world", "user1@example.com"),
        Message("This is spam!", "user2@example.com"),
        Message("Call 13800138000", "user3@example.com"),
        Message("Hi", "user4@example.com"),  # 太短
        Message("Normal message", "spammer@example.com"),  # 黑名单发件人
    ]
    
    # 过滤消息
    filtered = filter.filter_batch(messages)
    
    print(f"原始消息数: {len(messages)}")
    print(f"过滤后消息数: {len(filtered)}")
    for msg in filtered:
        print(f"- {msg.sender}: {msg.content}")