
import time
import threading
from datetime import datetime
from typing import Callable, Optional
import signal
import sys


class PeriodicTask:
    """周期任务执行器"""
    
    def __init__(self):
        self.tasks = []
        self.running = False
        self.threads = []
        
    def add_task(self, func: Callable, interval: float, name: Optional[str] = None):
        """添加周期任务
        
        Args:
            func: 要执行的函数
            interval: 执行间隔（秒）
            name: 任务名称
        """
        task = {
            'func': func,
            'interval': interval,
            'name': name or func.__name__,
            'stop_event': threading.Event()
        }
        self.tasks.append(task)
        
    def _run_task(self, task):
        """运行单个任务"""
        while not task['stop_event'].is_set():
            try:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行任务: {task['name']}")
                task['func']()
            except Exception as e:
                print(f"任务 {task['name']} 执行出错: {e}")
            
            task['stop_event'].wait(task['interval'])
    
    def start(self):
        """启动所有任务"""
        if self.running:
            print("任务已在运行中")
            return
            
        self.running = True
        print(f"启动 {len(self.tasks)} 个周期任务...")
        
        for task in self.tasks:
            thread = threading.Thread(target=self._run_task, args=(task,), daemon=True)
            thread.start()
            self.threads.append(thread)
    
    def stop(self):
        """停止所有任务"""
        if not self.running:
            return
            
        print("正在停止所有任务...")
        for task in self.tasks:
            task['stop_event'].set()
        
        for thread in self.threads:
            thread.join(timeout=2)
        
        self.running = False
        print("所有任务已停止")


class TaskScheduler:
    """装饰器风格的任务调度器"""
    
    def __init__(self):
        self.executor = PeriodicTask()
        
    def every(self, seconds: float):
        """装饰器：每隔指定秒数执行"""
        def decorator(func):
            self.executor.add_task(func, seconds)
            return func
        return decorator
    
    def start(self):
        """启动调度器"""
        self.executor.start()
        
    def stop(self):
        """停止调度器"""
        self.executor.stop()
    
    def run_forever(self):
        """持续运行直到收到中断信号"""
        def signal_handler(sig, frame):
            print("\n收到中断信号，正在退出...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        self.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()


# 使用示例

# 方式1: 直接使用 PeriodicTask
def task1():
    print("执行任务1 - 数据备份")

def task2():
    print("执行任务2 - 清理缓存")

def task3():
    print("执行任务3 - 健康检查")


# 方式2: 使用装饰器
scheduler = TaskScheduler()

@scheduler.every(5)
def check_system():
    print("系统检查完成")

@scheduler.every(10)
def sync_data():
    print("数据同步完成")

@scheduler.every(3)
def monitor_status():
    print("状态监控完成")


if __name__ == "__main__":
    # 选择一种方式运行
    
    # 方式1示例
    # executor = PeriodicTask()
    # executor.add_task(task1, 5, "备份任务")
    # executor.add_task(task2, 10, "清理任务")
    # executor.add_task(task3, 3, "健康检查")
    # executor.start()
    
    # 方式2示例（推荐）
    print("周期任务调度器启动，按 Ctrl+C 退出")
    scheduler.run_forever()
