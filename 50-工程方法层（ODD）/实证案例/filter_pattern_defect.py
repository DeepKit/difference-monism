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
        self.whitelist_mode: bool = False

    def add_keyword_blacklist(self, keywords: List[str]) -> None:
        self.keyword_blacklist.extend(keywords)

    def add_keyword_whitelist(self, keywords: List[str]) -> None:
        self.keyword_whitelist.extend(keywords)

    def add_pattern_blacklist(self, patterns: List[str]) -> None:
        self.pattern_blacklist.extend([re.compile(p, re.IGNORECASE) for p in patterns])

    def add_sender_blacklist(self, senders: List[str]) -> None:
        self.sender_blacklist.extend(senders)

    def add_sender_whitelist(self, senders: List[str]) -> None:
        self.sender_whitelist.extend(senders)

    def set_length_limits(self, min_length: Optional[int] = None, max_length: Optional[int] = None) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def add_custom_filter(self, filter_func: Callable[[Message], bool]) -> None:
        self.custom_filters.append(filter_func)

    def enable_whitelist_mode(self, enabled: bool = True) -> None:
        self.whitelist_mode = enabled

    def should_allow(self, message: Message) -> bool:
        # Whitelist mode: only allow if sender is whitelisted
        if self.whitelist_mode and self.sender_whitelist:
            if message.sender not in self.sender_whitelist:
                return False

        # Check sender blacklist
        if message.sender in self.sender_blacklist:
            return False

        # Check length limits
        if self.min_length and len(message.content) < self.min_length:
            return False
        if self.max_length and len(message.content) > self.max_length:
            return False

        # Check keyword blacklist
        content_lower = message.content.lower()
        for keyword in self.keyword_blacklist:
            if keyword.lower() in content_lower:
                return False

        # Check pattern blacklist
        for pattern in self.pattern_blacklist:
            if pattern.search(message.content):
                return False

        # Check custom filters (return False if any filter blocks)
        for custom_filter in self.custom_filters:
            if not custom_filter(message):
                return False

        return True

    def filter_messages(self, messages: List[Message]) -> List[Message]:
        return [msg for msg in messages if self.should_allow(msg)]

    def filter_message(self, message: Message) -> Optional[Message]:
        return message if self.should_allow(message) else None

    def clear_all_filters(self) -> None:
        self.keyword_blacklist.clear()
        self.keyword_whitelist.clear()
        self.pattern_blacklist.clear()
        self.sender_blacklist.clear()
        self.sender_whitelist.clear()
        self.custom_filters.clear()
        self.min_length = None
        self.max_length = None
        self.whitelist_mode = False


# 使用示例
if __name__ == "__main__":
    # 创建过滤器
    filter = MessageFilter()
    
    # 添加关键词黑名单
    filter.add_keyword_blacklist(["spam", "广告", "垃圾"])
    
    # 添加正则表达式黑名单
    filter.add_pattern_blacklist([r"\d{11}", r"http[s]?://\S+"])
    
    # 添加发送者黑名单
    filter.add_sender_blacklist(["spammer@example.com"])
    
    # 设置长度限制
    filter.set_length_limits(min_length=5, max_length=500)
    
    # 添加自定义过滤器
    filter.add_custom_filter(lambda msg: not msg.content.isupper())
    
    # 测试消息
    messages = [
        Message("Hello world", "user1@example.com"),
        Message("This is spam!", "user2@example.com"),
        Message("Call 13800138000", "user3@example.com"),
        Message("Hi", "user4@example.com"),
        Message("Normal message", "spammer@example.com"),
        Message("SHOUTING MESSAGE", "user5@example.com"),
    ]
    
    # 过滤消息
    filtered = filter.filter_messages(messages)
    
    print(f"原始消息数: {len(messages)}")
    print(f"过滤后消息数: {len(filtered)}")
    for msg in filtered:
        print(f"- {msg.sender}: {msg.content}")