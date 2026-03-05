import requests

API_KEY = 'fuyi-kiro-17781158558'
API_URL = 'http://localhost:8000/v1/chat/completions'

tasks = [
    ('test_t026', 'task_scheduler', 'TaskScheduler', '定时任务'),
    ('test_t027', 'delayed_task', 'DelayedTaskQueue', '延迟任务'),
    ('test_t028', 'periodic_task', 'PeriodicTaskManager', '周期任务'),
    ('test_t029', 'task_dependency', 'TaskDependencyManager', '任务依赖'),
    ('test_t030', 'task_timeout', 'TaskTimeoutHandler', '任务超时'),
    ('test_t031', 'distributed_lock', 'DistributedLock', '分布式锁'),
    ('test_t032', 'optimistic_lock', 'OptimisticLock', '乐观锁'),
    ('test_t033', 'pessimistic_lock', 'PessimisticLock', '悲观锁'),
    ('test_t034', 'semaphore', 'Semaphore', '信号量'),
    ('test_t035', 'rw_lock', 'ReadWriteLock', '读写锁'),
]

for test_file, module, classname, name in tasks:
    prompt = f'''pytest测试用例：测试{classname}类
基本功能测试，简洁的测试代码'''
    
    r = requests.post(API_URL, 
        headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
        json={'model': 'claude-sonnet-4.5', 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 4000})
    
    content = r.json()['choices'][0]['message']['content']
    if '```python' in content:
        code = content.split('```python')[1].split('```')[0]
    else:
        code = content
    
    filepath = f'D:/_Progs/01Center/ODD/实证案例/{test_file}.py'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f'Generated: {test_file}.py')

print('\nDone!')
