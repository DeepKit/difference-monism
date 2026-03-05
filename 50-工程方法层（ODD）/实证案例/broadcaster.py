
from typing import Callable, Dict, List, Any
from collections import defaultdict


class MessageBroadcaster:
    def __init__(self):
        self._channels: Dict[str, List[Callable]] = defaultdict(list)
    
    def subscribe(self, channel: str, callback: Callable[[Any], None]) -> None:
        """订阅指定通道"""
        if callback not in self._channels[channel]:
            self._channels[channel].append(callback)
    
    def unsubscribe(self, channel: str, callback: Callable[[Any], None]) -> bool:
        """取消订阅指定通道"""
        if callback in self._channels[channel]:
            self._channels[channel].remove(callback)
            return True
        return False
    
    def publish(self, channel: str, message: Any) -> int:
        """向指定通道发布消息，返回接收消息的订阅者数量"""
        count = 0
        for callback in self._channels[channel]:
            try:
                callback(message)
                count += 1
            except Exception as e:
                print(f"Error in callback: {e}")
        return count
    
    def clear(self, channel: str) -> None:
        """清空指定通道的所有订阅者"""
        self._channels[channel].clear()
    
    def clear_all(self) -> None:
        """清空所有通道"""
        self._channels.clear()
    
    def get_channels(self) -> List[str]:
        """获取所有通道名称"""
        return list(self._channels.keys())
    
    def get_subscriber_count(self, channel: str) -> int:
        """获取指定通道的订阅者数量"""
        return len(self._channels[channel])


# 使用示例
if __name__ == "__main__":
    broadcaster = MessageBroadcaster()
    
    # 定义订阅者回调函数
    def user1_handler(msg):
        print(f"User1 received: {msg}")
    
    def user2_handler(msg):
        print(f"User2 received: {msg}")
    
    def admin_handler(msg):
        print(f"Admin received: {msg}")
    
    # 订阅通道
    broadcaster.subscribe("news", user1_handler)
    broadcaster.subscribe("news", user2_handler)
    broadcaster.subscribe("alerts", admin_handler)
    broadcaster.subscribe("alerts", user1_handler)
    
    # 发布消息
    print("Publishing to 'news' channel:")
    broadcaster.publish("news", "Breaking news!")
    
    print("\nPublishing to 'alerts' channel:")
    broadcaster.publish("alerts", "System alert!")
    
    # 取消订阅
    print("\nUnsubscribing user1 from 'news':")
    broadcaster.unsubscribe("news", user1_handler)
    broadcaster.publish("news", "Another news update")
    
    # 查看通道信息
    print(f"\nChannels: {broadcaster.get_channels()}")
    print(f"Subscribers in 'news': {broadcaster.get_subscriber_count('news')}")
