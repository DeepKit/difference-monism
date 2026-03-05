import redis
import json
import time
import uuid
import traceback
from typing import Any, Callable, Optional, Dict, List
from datetime import datetime, timedelta
from enum import Enum
import threading
import signal
import sys


class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"


class RedisTaskQueue:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        queue_name: str = "default",
        max_retries: int = 3,
        retry_delay: int = 60,
        task_timeout: int = 3600,
        result_ttl: int = 86400
    ):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True
        )
        self.queue_name = queue_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.task_timeout = task_timeout
        self.result_ttl = result_ttl
        
        self.queue_key = f"queue:{queue_name}"
        self.processing_key = f"processing:{queue_name}"
        self.retry_key = f"retry:{queue_name}"
        self.task_data_key = f"task_data:{queue_name}"
        self.result_key = f"result:{queue_name}"
        
        self._running = False
        self._worker_thread = None
        
        try:
            self.redis_client.ping()
        except redis.ConnectionError as e:
            raise ConnectionError(f"无法连接到Redis: {e}")

    def enqueue(self, task_name: str, task_data: Dict[str, Any], priority: int = 0) -> str:
        try:
            task_id = str(uuid.uuid4())
            task = {
                "task_id": task_id,
                "task_name": task_name,
                "task_data": task_data,
                "status": TaskStatus.PENDING.value,
                "priority": priority,
                "retry_count": 0,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            pipe = self.redis_client.pipeline()
            pipe.hset(self.task_data_key, task_id, json.dumps(task))
            pipe.zadd(self.queue_key, {task_id: -priority})
            pipe.execute()
            
            return task_id
        except Exception as e:
            raise RuntimeError(f"任务入队失败: {e}")

    def dequeue(self, timeout: int = 0) -> Optional[Dict[str, Any]]:
        try:
            if timeout > 0:
                result = self.redis_client.bzpopmin(self.queue_key, timeout)
                if not result:
                    return None
                _, task_id, _ = result
            else:
                result = self.redis_client.zpopmin(self.queue_key, 1)
                if not result:
                    return None
                task_id, _ = result[0]
            
            task_json = self.redis_client.hget(self.task_data_key, task_id)
            if not task_json:
                return None
            
            task = json.loads(task_json)
            task["status"] = TaskStatus.PROCESSING.value
            task["updated_at"] = datetime.now().isoformat()
            task["processing_started_at"] = datetime.now().isoformat()
            
            pipe = self.redis_client.pipeline()
            pipe.hset(self.task_data_key, task_id, json.dumps(task))
            pipe.zadd(self.processing_key, {task_id: time.time()})
            pipe.execute()
            
            return task
        except Exception as e:
            raise RuntimeError(f"任务出队失败: {e}")

    def complete_task(self, task_id: str, result: Any = None) -> bool:
        try:
            task_json = self.redis_client.hget(self.task_data_key, task_id)
            if not task_json:
                return False
            
            task = json.loads(task_json)
            task["status"] = TaskStatus.COMPLETED.value
            task["updated_at"] = datetime.now().isoformat()
            task["completed_at"] = datetime.now().isoformat()
            
            pipe = self.redis_client.pipeline()
            pipe.hset(self.task_data_key, task_id, json.dumps(task))
            pipe.zrem(self.processing_key, task_id)
            
            if result is not None:
                result_data = {
                    "task_id": task_id,
                    "result": result,
                    "completed_at": datetime.now().isoformat()
                }
                pipe.setex(f"{self.result_key}:{task_id}", self.result_ttl, json.dumps(result_data))
            
            pipe.execute()
            return True
        except Exception as e:
            raise RuntimeError(f"完成任务失败: {e}")

    def fail_task(self, task_id: str, error: str) -> bool:
        try:
            task_json = self.redis_client.hget(self.task_data_key, task_id)
            if not task_json:
                return False
            
            task = json.loads(task_json)
            task["retry_count"] += 1
            task["updated_at"] = datetime.now().isoformat()
            task["last_error"] = error
            
            pipe = self.redis_client.pipeline()
            pipe.zrem(self.processing_key, task_id)
            
            if task["retry_count"] < self.max_retries:
                task["status"] = TaskStatus.RETRY.value
                retry_time = time.time() + self.retry_delay
                pipe.zadd(self.retry_key, {task_id: retry_time})
            else:
                task["status"] = TaskStatus.FAILED.value
                task["failed_at"] = datetime.now().isoformat()
            
            pipe.hset(self.task_data_key, task_id, json.dumps(task))
            pipe.execute()
            
            return True
        except Exception as e:
            raise RuntimeError(f"标记任务失败: {e}")

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        try:
            task_json = self.redis_client.hget(self.task_data_key, task_id)
            if not task_json:
                return None
            return json.loads(task_json)
        except Exception as e:
            raise RuntimeError(f"获取任务状态失败: {e}")

    def get_task_result(self, task_id: str) -> Optional[Any]:
        try:
            result_json = self.redis_client.get(f"{self.result_key}:{task_id}")
            if not result_json:
                return None
            result_data = json.loads(result_json)
            return result_data.get("result")
        except Exception as e:
            raise RuntimeError(f"获取任务结果失败: {e}")

    def requeue_retry_tasks(self) -> int:
        try:
            current_time = time.time()
            tasks = self.redis_client.zrangebyscore(self.retry_key, 0, current_time)
            
            if not tasks:
                return 0
            
            pipe = self.redis_client.pipeline()
            for task_id in tasks:
                task_json = self.redis_client.hget(self.task_data_key, task_id)
                if task_json:
                    task = json.loads(task_json)
                    task["status"] = TaskStatus.PENDING.value
                    task["updated_at"] = datetime.now().isoformat()
                    pipe.hset(self.task_data_key, task_id, json.dumps(task))
                    pipe.zadd(self.queue_key, {task_id: -task.get("priority", 0)})
                    pipe.zrem(self.retry_key, task_id)
            
            pipe.execute()
            return len(tasks)
        except Exception as e:
            raise RuntimeError(f"重新入队重试任务失败: {e}")

    def cleanup_stale_tasks(self) -> int:
        try:
            current_time = time.time()
            stale_time = current_time - self.task_timeout
            stale_tasks = self.redis_client.zrangebyscore(self.processing_key, 0, stale_time)
            
            if not stale_tasks:
                return 0
            
            for task_id in stale_tasks:
                self.fail_task(task_id, "任务超时")
            
            return len(stale_tasks)
        except Exception as e:
            raise RuntimeError(f"清理过期任务失败: {e}")

    def get_queue_size(self) -> int:
        try:
            return self.redis_client.zcard(self.queue_key)
        except Exception as e:
            raise RuntimeError(f"获取队列大小失败: {e}")

    def get_processing_count(self) -> int:
        try:
            return self.redis_client.zcard(self.processing_key)
        except Exception as e:
            raise RuntimeError(f"获取处理中任务数失败: {e}")

    def clear_queue(self) -> bool:
        try:
            pipe = self.redis_client.pipeline()
            pipe.delete(self.queue_key)
            pipe.delete(self.processing_key)
            pipe.delete(self.retry_key)
            pipe.delete(self.task_data_key)
            pipe.execute()
            return True
        except Exception as e:
            raise RuntimeError(f"清空队列失败: {e}")

    def register_task_handler(self, task_name: str, handler: Callable) -> None:
        if not hasattr(self, "_handlers"):
            self._handlers = {}
        self._handlers[task_name] = handler

    def start_worker(self, num_threads: int = 1) -> None:
        if self._running:
            raise RuntimeError("Worker已在运行")
        
        self._running = True
        
        def signal_handler(sig, frame):
            self.stop_worker()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self._worker_loop, daemon=True)
            thread.start()
            threads.append(thread)
        
        self._worker_threads = threads
        
        for thread in threads:
            thread.join()

    def stop_worker(self) -> None:
        self._running = False

    def _worker_loop(self) -> None:
        if not hasattr(self, "_handlers"):
            self._handlers = {}
        
        while self._running:
            try:
                self.requeue_retry_tasks()
                self.cleanup_stale_tasks()
                
                task = self.dequeue(timeout=1)
                if not task:
                    continue
                
                task_id = task["task_id"]
                task_name = task["task_name"]
                task_data = task["task_data"]
                
                handler = self._handlers.get(task_name)
                if not handler:
                    self.fail_task(task_id, f"未找到任务处理器: {task_name}")
                    continue
                
                try:
                    result = handler(task_data)
                    self.complete_task(task_id, result)
                except Exception as e:
                    error_msg = f"{str(e)}\n{traceback.format_exc()}"
                    self.fail_task(task_id, error_msg)
                    
            except Exception as e:
                print(f"Worker错误: {e}")
                time.sleep(1)

    def get_statistics(self) -> Dict[str, int]:
        try:
            return {
                "pending": self.get_queue_size(),
                "processing": self.get_processing_count(),
                "retry": self.redis_client.zcard(self.retry_key),
                "total_tasks": self.redis_client.hlen(self.task_data_key)
            }
        except Exception as e:
            raise RuntimeError(f"获取统计信息失败: {e}")

    def close(self) -> None:
        try:
            self.stop_worker()
            self.redis_client.close()
        except Exception as e:
            raise RuntimeError(f"关闭连接失败: {e}")