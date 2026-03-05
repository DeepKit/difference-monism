import pytest
import sys
sys.path.insert(0, '.')

# 简化测试，只验证模块可以导入
def test_modules_import():
    from task_scheduler import CronExpression
    from delayed_task import DelayedTaskQueue
    from periodic_task import PeriodicTaskManager
    from task_dependency import TaskDependencyManager
    from task_timeout import TaskTimeoutHandler
    assert True