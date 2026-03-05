import requests

API_KEY = 'fuyi-kiro-17781158558'
API_URL = 'http://localhost:8000/v1/chat/completions'

tasks = [
    ('task_scheduler.py', 'TaskScheduler', '定时任务调度器：cron表达式、周期任务、一次性任务'),
    ('delayed_task.py', 'DelayedTaskQueue', '延迟任务队列：延迟执行、超时处理'),
    ('periodic_task.py', 'PeriodicTaskManager', '周期任务管理：间隔任务、定时触发'),
    ('task_dependency.py', 'TaskDependencyManager', '任务依赖管理：DAG拓扑、依赖排序'),
    ('task_timeout.py', 'TaskTimeoutHandler', '任务超时处理：超时检测、超时回调'),
    ('distributed_lock.py', 'DistributedLock', '分布式锁：Redis实现、锁获取释放'),
    ('optimistic_lock.py', 'OptimisticLock', '乐观锁：版本号CAS、冲突重试'),
    ('pessimistic_lock.py', 'PessimisticLock', '悲观锁：数据库行锁、阻塞等待'),
    ('semaphore.py', 'Semaphore', '信号量控制：并发限制、资源池'),
    ('rw_lock.py', 'ReadWriteLock', '读写锁：读多写少、优化并发'),
]

results = []
for filename, classname, req in tasks:
    prompt = f'Python实现{classname}类：{req}。直接给完整代码，只回答代码'
    r = requests.post(API_URL, 
        headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
        json={'model': 'claude-sonnet-4.5', 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 8000})
    
    content = r.json()['choices'][0]['message']['content']
    if '```python' in content:
        code = content.split('```python')[1].split('```')[0]
    else:
        code = content
    
    filepath = f'D:/_Progs/01Center/ODD/实证案例/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f'Generated: {filename}')

print('\nDone!')
