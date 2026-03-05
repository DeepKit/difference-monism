import pytest
import time
from task_queue import TaskQueue, Priority, TaskStatus


def simple_task(x, y):
    return x + y


def slow_task(duration):
    time.sleep(duration)
    return "completed"


def failing_task():
    raise ValueError("Task failed intentionally")


def intermittent_task(fail_count=[0]):
    fail_count[0] += 1
    if fail_count[0] < 3:
        raise ValueError(f"Attempt {fail_count[0]} failed")
    return "success after retries"


class TestTaskQueue:
    
    def test_add_and_execute_task(self):
        queue = TaskQueue()
        queue.start()
        
        task_id = queue.add_task(simple_task, args=(5, 3))
        queue.wait_completion(timeout=2)
        
        status = queue.get_task_status(task_id)
        assert status["status"] == TaskStatus.COMPLETED.value
        assert status["result"] == 8
        
        queue.stop()
    
    def test_priority_execution(self):
        queue = TaskQueue()
        results = []
        
        def record_task(value):
            results.append(value)
            time.sleep(0.1)
        
        queue.add_task(record_task, args=("low",), priority=Priority.LOW)
        queue.add_task(record_task, args=("high",), priority=Priority.HIGH)
        queue.add_task(record_task, args=("normal",), priority=Priority.NORMAL)
        
        queue.start()
        queue.wait_completion(timeout=3)
        
        assert results[0] == "high"
        assert results[1] == "normal"
        assert results[2] == "low"
        
        queue.stop()
    
    def test_task_timeout(self):
        queue = TaskQueue()
        queue.start()
        
        task_id = queue.add_task(slow_task, args=(2,), timeout=0.5)
        queue.wait_completion(timeout=3)
        
        status = queue.get_task_status(task_id)
        assert status["status"] == TaskStatus.FAILED.value
        assert "timed out" in status["error"]
        
        queue.stop()
    
    def test_task_retry(self):
        queue = TaskQueue()
        queue.start()
        
        fail_count = [0]
        task_id = queue.add_task(
            intermittent_task,
            args=(fail_count,),
            max_retries=3
        )
        queue.wait_completion(timeout=3)
        
        status = queue.get_task_status(task_id)
        assert status["status"] == TaskStatus.COMPLETED.value
        assert status["result"] == "success after retries"
        assert status["retries"] == 2
        
        queue.stop()
    
    def test_task_max_retries_exceeded(self):
        queue = TaskQueue()
        queue.start()
        
        task_id = queue.add_task(failing_task, max_retries=2)
        queue.wait_completion(timeout=3)
        
        status = queue.get_task_status(task_id)
        assert status["status"] == TaskStatus.FAILED.value
        assert "failed intentionally" in status["error"]
        assert status["retries"] == 2
        
        queue.stop()
    
    def test_multiple_tasks(self):
        queue = TaskQueue()
        queue.start()
        
        task_ids = []
        for i in range(5):
            task_id = queue.add_task(simple_task, args=(i, i))
            task_ids.append(task_id)
        
        queue.wait_completion(timeout=3)
        
        for i, task_id in enumerate(task_ids):
            status = queue.get_task_status(task_id)
            assert status["status"] == TaskStatus.COMPLETED.value
            assert status["result"] == i * 2
        
        queue.stop()
    
    def test_task_with_kwargs(self):
        queue = TaskQueue()
        queue.start()
        
        def task_with_kwargs(a, b=10):
            return a + b
        
        task_id = queue.add_task(
            task_with_kwargs,
            args=(5,),
            kwargs={"b": 20}
        )
        queue.wait_completion(timeout=2)
        
        status = queue.get_task_status(task_id)
        assert status["status"] == TaskStatus.COMPLETED.value
        assert status["result"] == 25
        
        queue.stop()
    
    def test_get_nonexistent_task(self):
        queue = TaskQueue()
        status = queue.get_task_status("nonexistent_id")
        assert status is None
    
    def test_task_error_message(self):
        queue = TaskQueue()
        queue.start()
        
        def error_task():
            raise RuntimeError("Custom error message")
        
        task_id = queue.add_task(error_task, max_retries=0)
        queue.wait_completion(timeout=2)
        
        status = queue.get_task_status(task_id)
        assert status["status"] == TaskStatus.FAILED.value
        assert "Custom error message" in status["error"]
        
        queue.stop()
