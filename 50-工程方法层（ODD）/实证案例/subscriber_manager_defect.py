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
        self.subscribers: Dict[str, Subscriber] = {}
    
    def add_subscriber(self, email: str, name: str = "", tags: List[str] = None) -> bool:
        """添加订阅者"""
        if not self._validate_email(email):
            raise ValueError(f"无效的邮箱地址: {email}")
        
        if email in self.subscribers:
            return False
        
        self.subscribers[email] = Subscriber(email, name, tags)
        return True
    
    def remove_subscriber(self, email: str) -> bool:
        """删除订阅者"""
        if email in self.subscribers:
            del self.subscribers[email]
            return True
        return False
    
    def deactivate_subscriber(self, email: str) -> bool:
        """停用订阅者"""
        if email in self.subscribers:
            self.subscribers[email].is_active = False
            return True
        return False
    
    def activate_subscriber(self, email: str) -> bool:
        """激活订阅者"""
        if email in self.subscribers:
            self.subscribers[email].is_active = True
            return True
        return False
    
    def get_subscriber(self, email: str) -> Optional[Subscriber]:
        """获取订阅者"""
        return self.subscribers.get(email)
    
    def update_subscriber(self, email: str, name: str = None, tags: List[str] = None) -> bool:
        """更新订阅者信息"""
        if email not in self.subscribers:
            return False
        
        subscriber = self.subscribers[email]
        if name is not None:
            subscriber.name = name
        if tags is not None:
            subscriber.tags = tags
        return True
    
    def add_tags(self, email: str, tags: List[str]) -> bool:
        """添加标签"""
        if email not in self.subscribers:
            return False
        
        subscriber = self.subscribers[email]
        subscriber.tags.extend([tag for tag in tags if tag not in subscriber.tags])
        return True
    
    def remove_tags(self, email: str, tags: List[str]) -> bool:
        """移除标签"""
        if email not in self.subscribers:
            return False
        
        subscriber = self.subscribers[email]
        subscriber.tags = [tag for tag in subscriber.tags if tag not in tags]
        return True
    
    def get_all_subscribers(self, active_only: bool = False) -> List[Subscriber]:
        """获取所有订阅者"""
        subscribers = list(self.subscribers.values())
        if active_only:
            subscribers = [s for s in subscribers if s.is_active]
        return subscribers
    
    def search_by_tag(self, tag: str) -> List[Subscriber]:
        """按标签搜索"""
        return [s for s in self.subscribers.values() if tag in s.tags]
    
    def search_by_name(self, name: str) -> List[Subscriber]:
        """按名称搜索"""
        name_lower = name.lower()
        return [s for s in self.subscribers.values() if name_lower in s.name.lower()]
    
    def get_count(self, active_only: bool = False) -> int:
        """获取订阅者数量"""
        if active_only:
            return sum(1 for s in self.subscribers.values() if s.is_active)
        return len(self.subscribers)
    
    def export_to_json(self, filepath: str):
        """导出到JSON文件"""
        data = {email: sub.to_dict() for email, sub in self.subscribers.items()}
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def import_from_json(self, filepath: str):
        """从JSON文件导入"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for email, sub_data in data.items():
            self.subscribers[email] = Subscriber.from_dict(sub_data)
    
    def bulk_add(self, subscribers: List[Dict]) -> Dict[str, int]:
        """批量添加订阅者"""
        results = {'success': 0, 'failed': 0, 'duplicate': 0}
        
        for sub_data in subscribers:
            email = sub_data.get('email')
            if not email:
                results['failed'] += 1
                continue
            
            if email in self.subscribers:
                results['duplicate'] += 1
                continue
            
            try:
                self.add_subscriber(
                    email,
                    sub_data.get('name', ''),
                    sub_data.get('tags', [])
                )
                results['success'] += 1
            except ValueError:
                results['failed'] += 1
        
        return results
    
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
    
    # 批量添加
    bulk_data = [
        {"email": "user3@example.com", "name": "王五", "tags": ["VIP"]},
        {"email": "user4@example.com", "name": "赵六"}
    ]
    results = manager.bulk_add(bulk_data)
    print(f"批量添加结果: {results}")
    
    # 搜索
    vip_users = manager.search_by_tag("VIP")
    print(f"VIP用户数: {len(vip_users)}")
    
    # 更新
    manager.add_tags("user1@example.com", ["新标签"])
    
    # 统计
    print(f"总订阅者数: {manager.get_count()}")
    
    # 导出
    manager.export_to_json("subscribers.json")