from datetime import datetime
from typing import List, Optional, Dict
import json


class Subscriber:
    """订阅者实体类"""
    
    def __init__(self, email: str, name: str = "", tags: List[str] = None):
        self.email = email
        self.name = name
        self.tags = tags or []
        self.subscribed_at = datetime.now()
        self.is_active = True
        self.metadata = {}
    
    def to_dict(self) -> Dict:
        return {
            'email': self.email,
            'name': self.name,
            'tags': self.tags,
            'subscribed_at': self.subscribed_at.isoformat(),
            'is_active': self.is_active,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Subscriber':
        subscriber = cls(data['email'], data.get('name', ''), data.get('tags', []))
        subscriber.subscribed_at = datetime.fromisoformat(data['subscribed_at'])
        subscriber.is_active = data.get('is_active', True)
        subscriber.metadata = data.get('metadata', {})
        return subscriber


class SubscriberManager:
    """订阅者管理类"""
    
    def __init__(self):
        self._subscribers: Dict[str, Subscriber] = {}
    
    def add_subscriber(self, email: str, name: str = "", tags: List[str] = None) -> bool:
        """添加订阅者"""
        if not self._validate_email(email):
            raise ValueError(f"无效的邮箱地址: {email}")
        
        if email in self._subscribers:
            return False
        
        self._subscribers[email] = Subscriber(email, name, tags)
        return True
    
    def remove_subscriber(self, email: str) -> bool:
        """删除订阅者"""
        if email in self._subscribers:
            del self._subscribers[email]
            return True
        return False
    
    def get_subscriber(self, email: str) -> Optional[Subscriber]:
        """获取订阅者"""
        return self._subscribers.get(email)
    
    def update_subscriber(self, email: str, name: str = None, tags: List[str] = None) -> bool:
        """更新订阅者信息"""
        subscriber = self.get_subscriber(email)
        if not subscriber:
            return False
        
        if name is not None:
            subscriber.name = name
        if tags is not None:
            subscriber.tags = tags
        
        return True
    
    def deactivate_subscriber(self, email: str) -> bool:
        """停用订阅者"""
        subscriber = self.get_subscriber(email)
        if subscriber:
            subscriber.is_active = False
            return True
        return False
    
    def activate_subscriber(self, email: str) -> bool:
        """激活订阅者"""
        subscriber = self.get_subscriber(email)
        if subscriber:
            subscriber.is_active = True
            return True
        return False
    
    def get_all_subscribers(self, active_only: bool = True) -> List[Subscriber]:
        """获取所有订阅者"""
        subscribers = list(self._subscribers.values())
        if active_only:
            subscribers = [s for s in subscribers if s.is_active]
        return subscribers
    
    def search_by_tag(self, tag: str) -> List[Subscriber]:
        """按标签搜索订阅者"""
        return [s for s in self._subscribers.values() if tag in s.tags and s.is_active]
    
    def search_by_name(self, name: str) -> List[Subscriber]:
        """按名称搜索订阅者"""
        name_lower = name.lower()
        return [s for s in self._subscribers.values() 
                if name_lower in s.name.lower() and s.is_active]
    
    def get_subscriber_count(self, active_only: bool = True) -> int:
        """获取订阅者数量"""
        if active_only:
            return sum(1 for s in self._subscribers.values() if s.is_active)
        return len(self._subscribers)
    
    def add_tag_to_subscriber(self, email: str, tag: str) -> bool:
        """为订阅者添加标签"""
        subscriber = self.get_subscriber(email)
        if subscriber and tag not in subscriber.tags:
            subscriber.tags.append(tag)
            return True
        return False
    
    def remove_tag_from_subscriber(self, email: str, tag: str) -> bool:
        """移除订阅者标签"""
        subscriber = self.get_subscriber(email)
        if subscriber and tag in subscriber.tags:
            subscriber.tags.remove(tag)
            return True
        return False
    
    def export_to_json(self, filepath: str):
        """导出到JSON文件"""
        data = [s.to_dict() for s in self._subscribers.values()]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def import_from_json(self, filepath: str):
        """从JSON文件导入"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            subscriber = Subscriber.from_dict(item)
            self._subscribers[subscriber.email] = subscriber
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """验证邮箱格式"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


# 使用示例
if __name__ == "__main__":
    manager = SubscriberManager()
    
    # 添加订阅者
    manager.add_subscriber("user1@example.com", "张三", ["VIP", "技术"])
    manager.add_subscriber("user2@example.com", "李四", ["普通"])
    manager.add_subscriber("user3@example.com", "王五", ["VIP"])
    
    # 获取所有订阅者
    print(f"总订阅者数: {manager.get_subscriber_count()}")
    
    # 按标签搜索
    vip_subscribers = manager.search_by_tag("VIP")
    print(f"VIP订阅者数: {len(vip_subscribers)}")
    
    # 更新订阅者
    manager.update_subscriber("user1@example.com", name="张三丰")
    
    # 停用订阅者
    manager.deactivate_subscriber("user2@example.com")
    print(f"活跃订阅者数: {manager.get_subscriber_count(active_only=True)}")
    
    # 导出数据
    manager.export_to_json("subscribers.json")