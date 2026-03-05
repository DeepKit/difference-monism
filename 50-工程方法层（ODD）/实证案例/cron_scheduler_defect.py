import time
import threading
from datetime import datetime
from typing import Callable, Dict, List, Set


class CronScheduler:
    def __init__(self):
        self.jobs: Dict[str, Dict] = {}
        self.running = False
        self.thread = None

    def parse_cron_field(self, field: str, min_val: int, max_val: int) -> Set[int]:
        """解析单个cron字段"""
        if field == '*':
            return set(range(min_val, max_val + 1))
        
        values = set()
        for part in field.split(','):
            if '/' in part:
                range_part, step = part.split('/')
                step = int(step)
                if range_part == '*':
                    values.update(range(min_val, max_val + 1, step))
                else:
                    start, end = map(int, range_part.split('-'))
                    values.update(range(start, end + 1, step))
            elif '-' in part:
                start, end = map(int, part.split('-'))
                values.update(range(start, end + 1))
            else:
                values.add(int(part))
        
        return values

    def parse_cron(self, cron_expr: str) -> Dict[str, Set[int]]:
        """解析cron表达式: 分 时 日 月 周"""
        parts = cron_expr.split()
        if len(parts) != 5:
            raise ValueError("Cron表达式格式错误，应为: 分 时 日 月 周")
        
        return {
            'minute': self.parse_cron_field(parts[0], 0, 59),
            'hour': self.parse_cron_field(parts[1], 0, 23),
            'day': self.parse_cron_field(parts[2], 1, 31),
            'month': self.parse_cron_field(parts[3], 1, 12),
            'weekday': self.parse_cron_field(parts[4], 0, 6)
        }

    def should_run(self, cron_time: Dict[str, Set[int]], now: datetime) -> bool:
        """检查当前时间是否匹配cron表达式"""
        return (
            now.minute in cron_time['minute'] and
            now.hour in cron_time['hour'] and
            now.day in cron_time['day'] and
            now.month in cron_time['month'] and
            now.weekday() in cron_time['weekday']
        )

    def add_job(self, name: str, cron_expr: str, func: Callable, *args, **kwargs):
        """添加定时任务"""
        cron_time = self.parse_cron(cron_expr)
        self.jobs[name] = {
            'cron_time': cron_time,
            'func': func,
            'args': args,
            'kwargs': kwargs,
            'last_run': None
        }

    def remove_job(self, name: str):
        """移除定时任务"""
        if name in self.jobs:
            del self.jobs[name]

    def _run_loop(self):
        """调度循环"""
        while self.running:
            now = datetime.now().replace(second=0, microsecond=0)
            
            for name, job in self.jobs.items():
                if job['last_run'] != now and self.should_run(job['cron_time'], now):
                    job['last_run'] = now
                    try:
                        threading.Thread(
                            target=job['func'],
                            args=job['args'],
                            kwargs=job['kwargs']
                        ).start()
                    except Exception as e:
                        print(f"任务 {name} 执行失败: {e}")
            
            time.sleep(1)

    def start(self):
        """启动调度器"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()

    def stop(self):
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join()


# 使用示例
if __name__ == '__main__':
    def task1():
        print(f"[{datetime.now()}] 任务1执行")

    def task2(msg):
        print(f"[{datetime.now()}] 任务2: {msg}")

    scheduler = CronScheduler()
    
    # 每分钟执行
    scheduler.add_job('job1', '* * * * *', task1)
    
    # 每小时的第30分钟执行
    scheduler.add_job('job2', '30 * * * *', task2, "每小时执行")
    
    # 每天早上9点执行
    # scheduler.add_job('job3', '0 9 * * *', task1)
    
    scheduler.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()