import redis
import json
import uuid
from typing import Any, Optional


class RedisTaskQueue:
    def __init__(self, host='localhost', port=6379, db=0, queue_name='task_queue'):
        """初始化Redis任务队列"""
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.queue_name = queue_name
        self.processing_key = f"{queue_name}:processing"
    
    def enqueue(self, task: Any, priority: int = 0) -> str:
        """添加任务到队列，返回任务ID"""
        task_id = str(uuid.uuid4())
        task_data = {
            'id': task_id,
            'data': task,
            'priority': priority
        }
        self.client.zadd(self.queue_name, {json.dumps(task_data): priority})
        return task_id
    
    def dequeue(self, timeout: int = 0) -> Optional[dict]:
        """从队列取出任务（按优先级）"""
        if timeout > 0:
            result = self.client.bzpopmin(self.queue_name, timeout=timeout)
        else:
            result = self.client.zpopmin(self.queue_name, count=1)
            result = result[0] if result else None
        
        if result:
            task_json = result[0] if timeout > 0 else result[0]
            return json.loads(task_json)
        return None
    
    def size(self) -> int:
        """获取队列长度"""
        return self.client.zcard(self.queue_name)
    
    def clear(self):
        """清空队列"""
        self.client.delete(self.queue_name)
    
    def peek(self, count: int = 1) -> list:
        """查看队列前N个任务（不移除）"""
        results = self.client.zrange(self.queue_name, 0, count - 1)
        return [json.loads(task) for task in results]


# 使用示例
if __name__ == '__main__':
    queue = RedisTaskQueue()
    
    # 添加任务
    queue.enqueue({'action': 'send_email', 'to': 'user@example.com'}, priority=1)
    queue.enqueue({'action': 'process_data', 'file': 'data.csv'}, priority=5)
    
    # 取出任务
    task = queue.dequeue()
    print(f"处理任务: {task}")
    
    # 查看队列大小
    print(f"队列长度: {queue.size()}")