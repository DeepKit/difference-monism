import re
import time
import threading
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CronJob:
    """表示一个定时任务"""
    name: str
    cron_expression: str
    callback: Callable
    args: tuple = ()
    kwargs: dict = None
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


class CronParser:
    """Cron表达式解析器"""
    
    FIELDS = ['minute', 'hour', 'day', 'month', 'weekday']
    RANGES = {
        'minute': (0, 59),
        'hour': (0, 23),
        'day': (1, 31),
        'month': (1, 12),
        'weekday': (0, 6)  # 0=周日, 6=周六
    }
    
    @staticmethod
    def parse(expression: str) -> Dict[str, List[int]]:
        """
        解析Cron表达式
        格式: 分 时 日 月 周
        支持: * , - / 符号
        """
        parts = expression.strip().split()
        if len(parts) != 5:
            raise ValueError(f"无效的Cron表达式: {expression}，应为5个字段")
        
        result = {}
        for i, (field, part) in enumerate(zip(CronParser.FIELDS, parts)):
            result[field] = CronParser._parse_field(part, field)
        
        return result
    
    @staticmethod
    def _parse_field(value: str, field: str) -> List[int]:
        """解析单个字段"""
        min_val, max_val = CronParser.RANGES[field]
        
        # 处理 *
        if value == '*':
            return list(range(min_val, max_val + 1))
        
        # 处理步长 */n 或 start-end/step
        if '/' in value:
            range_part, step = value.split('/')
            step = int(step)
            
            if range_part == '*':
                start, end = min_val, max_val
            elif '-' in range_part:
                start, end = map(int, range_part.split('-'))
            else:
                start = int(range_part)
                end = max_val
            
            return list(range(start, end + 1, step))
        
        # 处理范围 start-end
        if '-' in value:
            start, end = map(int, value.split('-'))
            return list(range(start, end + 1))
        
        # 处理列表 1,2,3
        if ',' in value:
            return [int(v) for v in value.split(',')]
        
        # 单个值
        return [int(value)]
    
    @staticmethod
    def should_run(cron_dict: Dict[str, List[int]], now: datetime) -> bool:
        """判断当前时间是否应该执行任务"""
        return (
            now.minute in cron_dict['minute'] and
            now.hour in cron_dict['hour'] and
            now.day in cron_dict['day'] and
            now.month in cron_dict['month'] and
            now.weekday() in [(d + 1) % 7 for d in cron_dict['weekday']]  # 转换周日为0
        )


class CronScheduler:
    """Cron调度器"""
    
    def __init__(self):
        self.jobs: Dict[str, Tuple[CronJob, Dict]] = {}
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        self._last_minute = None
    
    def add_job(
        self,
        name: str,
        cron_expression: str,
        callback: Callable,
        args: tuple = (),
        kwargs: dict = None
    ) -> None:
        """
        添加定时任务
        
        Args:
            name: 任务名称（唯一标识）
            cron_expression: Cron表达式，格式: 分 时 日 月 周
            callback: 回调函数
            args: 位置参数
            kwargs: 关键字参数
        """
        try:
            parsed = CronParser.parse(cron_expression)
            job = CronJob(name, cron_expression, callback, args, kwargs or {})
            
            with self.lock:
                self.jobs[name] = (job, parsed)
            
            logger.info(f"任务已添加: {name} - {cron_expression}")
        except Exception as e:
            logger.error(f"添加任务失败 {name}: {e}")
            raise
    
    def remove_job(self, name: str) -> bool:
        """删除任务"""
        with self.lock:
            if name in self.jobs:
                del self.jobs[name]
                logger.info(f"任务已删除: {name}")
                return True
            return False
    
    def get_jobs(self) -> List[str]:
        """获取所有任务名称"""
        with self.lock:
            return list(self.jobs.keys())
    
    def start(self, blocking: bool = False) -> None:
        """
        启动调度器
        
        Args:
            blocking: 是否阻塞当前线程
        """
        if self.running:
            logger.warning("调度器已在运行")
            return
        
        self.running = True
        logger.info("调度器已启动")
        
        if blocking:
            self._run()
        else:
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
    
    def stop(self) -> None:
        """停止调度器"""
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("调度器已停止")
    
    def _run(self) -> None:
        """主循环"""
        while self.running:
            try:
                now = datetime.now()
                current_minute = (now.year, now.month, now.day, now.hour, now.minute)
                
                # 避免同一分钟内重复执行
                if current_minute != self._last_minute:
                    self._last_minute = current_minute
                    self._check_and_run_jobs(now)
                
                # 每秒检查一次
                time.sleep(1)
            except Exception as e:
                logger.error(f"调度器运行错误: {e}")
    
    def _check_and_run_jobs(self, now: datetime) -> None:
        """检查并运行到期的任务"""
        with self.lock:
            jobs_to_run = []
            for name, (job, parsed) in self.jobs.items():
                if CronParser.should_run(parsed, now):
                    jobs_to_run.append(job)
        
        # 在锁外执行任务，避免阻塞
        for job in jobs_to_run:
            self._execute_job(job)
    
    def _execute_job(self, job: CronJob) -> None:
        """执行单个任务"""
        try:
            logger.info(f"执行任务: {job.name}")
            job.callback(*job.args, **job.kwargs)
        except Exception as e:
            logger.error(f"任务执行失败 {job.name}: {e}")


# 使用示例
if __name__ == "__main__":
    def task1():
        print(f"[{datetime.now()}] 任务1执行")
    
    def task2(message):
        print(f"[{datetime.now()}] 任务2: {message}")
    
    def task3(a, b):
        print(f"[{datetime.now()}] 任务3: {a} + {b} = {a + b}")
    
    # 创建调度器
    scheduler = CronScheduler()
    
    # 添加任务
    scheduler.add_job("task1", "* * * * *", task1)  # 每分钟
    scheduler.add_job("task2", "*/2 * * * *", task2, args=("Hello",))  # 每2分钟
    scheduler.add_job("task3", "*/5 * * * *", task3, kwargs={"a": 10, "b": 20})  # 每5分钟
    
    # 启动调度器
    scheduler.start()
    
    try:
        # 运行一段时间
        time.sleep(300)
    except KeyboardInterrupt:
        print("\n停止调度器...")
    finally:
        scheduler.stop()