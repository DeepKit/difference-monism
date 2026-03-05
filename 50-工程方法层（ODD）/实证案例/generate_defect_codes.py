"""
AI-First方式生成有缺陷的对照组代码
不提供详细契约，让AI自由理解需求
"""
import requests
import time

API_KEY = 'fuyi-kiro-17781158558'
API_URL = 'http://localhost:8000/v1/chat/completions'

tasks = [
    ('message_queue', '消息队列系统', '实现一个消息队列，支持发布订阅、持久化'),
    ('email_service', '邮件服务', '实现邮件发送服务，支持SMTP'),
    ('websocket_manager', 'WebSocket管理', '实现WebSocket连接管理器'),
    ('sse_server', 'SSE服务器', '实现Server-Sent Events服务器'),
    ('broadcaster', '消息广播', '实现消息广播器'),
    ('csv_exporter', 'CSV导出', '实现CSV文件导出功能'),
    ('excel_parser', 'Excel解析', '实现Excel文件解析'),
    ('json_validator', 'JSON验证', '实现JSON数据验证'),
    ('data_masker', '数据脱敏', '实现敏感数据掩码处理'),
    ('data_encryptor', '数据加密', '实现AES加密解密'),
    ('task_scheduler', '任务调度', '实现定时任务调度器'),
    ('delayed_task', '延迟任务', '实现延迟队列'),
    ('periodic_task', '周期任务', '实现周期性任务'),
    ('task_dependency', '任务依赖', '实现任务依赖管理'),
    ('task_timeout', '任务超时', '实现任务超时处理'),
    ('distributed_lock', '分布式锁', '实现分布式锁'),
    ('optimistic_lock', '乐观锁', '实现乐观锁'),
    ('pessimistic_lock', '悲观锁', '实现悲观锁'),
    ('semaphore', '信号量', '实现信号量'),
    ('rw_lock', '读写锁', '实现读写锁'),
    ('memory_cache', '内存缓存', '实现内存缓存'),
    ('disk_cache', '磁盘缓存', '实现磁盘缓存'),
    ('multi_level_cache', '多级缓存', '实现多级缓存'),
    ('cache_warming', '缓存预热', '实现缓存预热'),
    ('cache_invalidation', '缓存失效', '实现缓存失效策略'),
    ('jwt_token', 'JWT令牌', '实现JWT Token管理'),
    ('api_signature', 'API签名', '实现API签名验证'),
    ('rate_limiter_v2', '限流器', '实现请求限流'),
    ('csrf_protector', 'CSRF防护', '实现CSRF保护'),
    ('xss_filter', 'XSS过滤', '实现XSS过滤器'),
    ('order_state_machine', '订单状态机', '实现订单状态机'),
    ('workflow_engine', '工作流引擎', '实现工作流引擎'),
    ('rules_engine', '规则引擎', '实现规则引擎'),
    ('metrics_calculator', '指标计算', '实现业务指标计算'),
    ('report_generator', '报表生成', '实现报表生成'),
]

for filename, name, brief_req in tasks:
    prompt = f'用Python实现{name}，完整代码：{brief_req}。直接给出完整代码，不需要测试。'
    
    try:
        r = requests.post(API_URL, 
            headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
            json={'model': 'claude-sonnet-4.5', 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 8000})
        
        content = r.json()['choices'][0]['message']['content']
        
        # 提取代码
        if '```python' in content:
            code = content.split('```python')[1].split('```')[0]
        elif '```' in content:
            code = content.split('```')[1].split('```')[0]
        else:
            code = content
        
        # 写入文件
        with open(f'D:/_Progs/01Center/ODD/实证案例/{filename}_defect.py', 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f'Generated: {filename}_defect.py')
        time.sleep(1)  # 避免API限流
        
    except Exception as e:
        print(f'Error {filename}: {e}')

print('Done!')
