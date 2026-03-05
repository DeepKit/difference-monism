from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass, field
import hashlib


@dataclass
class Comment:
    comment_id: str
    user_id: str
    content: str
    parent_id: Optional[str] = None
    level: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {'comment_id': self.comment_id, 'user_id': self.user_id, 'content': self.content, 'parent_id': self.parent_id, 'level': self.level, 'created_at': self.created_at.isoformat()}


class CommentSystem:
    SENSITIVE_WORDS = {'政治', '政府', '领导人', '革命', '政权', '色情', '黄色', '裸体', '性交', '淫秽', '暴力', '杀人', '血腥', '恐怖', '枪支', '爆炸'}
    MIN_CONTENT_LENGTH = 5
    MAX_CONTENT_LENGTH = 500
    MAX_REPLY_LEVEL = 2
    DUPLICATE_CHECK_MINUTES = 5
    
    def __init__(self):
        self.comments: Dict[str, Comment] = {}
        self.comment_counter = 0
        self.recent_comments: Dict[str, List[tuple]] = {}
    
    def _generate_comment_id(self) -> str:
        self.comment_counter += 1
        return f"comment_{self.comment_counter}"
    
    def _validate_content_length(self, content: str) -> tuple[bool, Optional[str]]:
        length = len(content)
        if length < self.MIN_CONTENT_LENGTH:
            return False, f"评论内容过短，至少需要{self.MIN_CONTENT_LENGTH}个字符"
        if length > self.MAX_CONTENT_LENGTH:
            return False, f"评论内容过长，最多允许{self.MAX_CONTENT_LENGTH}个字符"
        return True, None
    
    def _check_sensitive_words(self, content: str) -> tuple[bool, Optional[str]]:
        for word in self.SENSITIVE_WORDS:
            if word in content:
                return False, f"评论包含敏感词：{word}"
        return True, None
    
    def _get_content_hash(self, content: str) -> str:
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _check_duplicate(self, user_id: str, content: str) -> tuple[bool, Optional[str]]:
        if user_id not in self.recent_comments:
            return True, None
        
        content_hash = self._get_content_hash(content)
        current_time = datetime.now()
        time_threshold = current_time - timedelta(minutes=self.DUPLICATE_CHECK_MINUTES)
        
        self.recent_comments[user_id] = [(hash_val, timestamp) for hash_val, timestamp in self.recent_comments[user_id] if timestamp > time_threshold]
        
        for hash_val, timestamp in self.recent_comments[user_id]:
            if hash_val == content_hash:
                return False, f"请勿在{self.DUPLICATE_CHECK_MINUTES}分钟内发表相同内容"
        
        return True, None
    
    def _record_comment(self, user_id: str, content: str):
        if user_id not in self.recent_comments:
            self.recent_comments[user_id] = []
        content_hash = self._get_content_hash(content)
        self.recent_comments[user_id].append((content_hash, datetime.now()))
    
    def _validate_reply_level(self, parent_id: Optional[str]) -> tuple[bool, Optional[str], int]:
        if parent_id is None:
            return True, None, 0
        if parent_id not in self.comments:
            return False, "父评论不存在", 0
        parent_comment = self.comments[parent_id]
        new_level = parent_comment.level + 1
        if new_level > self.MAX_REPLY_LEVEL:
            return False, f"回复层级超过限制，最多支持{self.MAX_REPLY_LEVEL}层回复", 0
        return True, None, new_level
    
    def post_comment(self, user_id: str, content: str, parent_id: Optional[str] = None) -> dict:
        valid, error = self._validate_content_length(content)
        if not valid:
            return {'success': False, 'error': error}
        
        valid, error = self._check_sensitive_words(content)
        if not valid:
            return {'success': False, 'error': error}
        
        valid, error = self._check_duplicate(user_id, content)
        if not valid:
            return {'success': False, 'error': error}
        
        valid, error, level = self._validate_reply_level(parent_id)
        if not valid:
            return {'success': False, 'error': error}
        
        comment_id = self._generate_comment_id()
        comment = Comment(comment_id=comment_id, user_id=user_id, content=content, parent_id=parent_id, level=level)
        self.comments[comment_id] = comment
        self._record_comment(user_id, content)
        
        return {'success': True, 'data': comment.to_dict()}
    
    def get_comment(self, comment_id: str) -> Optional[dict]:
        comment = self.comments.get(comment_id)
        return comment.to_dict() if comment else None
    
    def get_replies(self, parent_id: str) -> List[dict]:
        replies = [comment.to_dict() for comment in self.comments.values() if comment.parent_id == parent_id]
        return sorted(replies, key=lambda x: x['created_at'])
    
    def get_all_comments(self) -> List[dict]:
        top_level = [comment.to_dict() for comment in self.comments.values() if comment.parent_id is None]
        return sorted(top_level, key=lambda x: x['created_at'], reverse=True)
