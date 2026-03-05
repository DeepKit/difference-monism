"""
继续生成有缺陷的对照组代码 - T-026~050
"""
import requests
import time

API_KEY = 'fuyi-kiro-17781158558'
API_URL = 'http://localhost:8000/v1/chat/completions'

tasks = [
    ('rw_lock', '读写锁', '实现读写锁'),
    ('memory_cache', '内存缓存', '实现内存缓存'),
    ('disk_cache', '磁盘缓存', '实现磁盘缓存'),
    ('multi_level_cache', '多级缓存', '实现多级缓存'),
    ('cache_warming', '缓存预热', '实现缓存预热'),
    ('cache_invalidation', '缓存失效', '实现缓存失效'),
    ('jwt_token', 'JWT令牌', '实现JWT Token'),
    ('api_signature', 'API签名', '实现API签名'),
    ('rate_limiter_v2', '限流器', '实现限流'),
    ('csrf_protector', 'CSRF防护', '实现CSRF保护'),
    ('xss_filter', 'XSS过滤', '实现XSS过滤'),
    ('order_state_machine', '订单状态机', '实现状态机'),
    ('workflow_engine', '工作流引擎', '实现工作流'),
    ('rules_engine', '规则引擎', '实现规则引擎'),
    ('metrics_calculator', '指标计算', '实现指标计算'),
    ('report_generator', '报表生成', '实现报表生成'),
]

for filename, name, brief_req in tasks:
    prompt = f'用Python实现{name}，完整代码：{brief_req}。直接给出完整代码，不需要测试。'
    
    try:
        r = requests.post(API_URL, 
            headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
            json={'model': 'claude-sonnet-4.5', 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 8000})
        
        content = r.json()['choices'][0]['message']['content']
        
        if '```python' in content:
            code = content.split('```python')[1].split('```')[0]
        elif '```' in content:
            code = content.split('```')[1].split('```')[0]
        else:
            code = content
        
        with open(f'D:/_Progs/01Center/ODD/实证案例/{filename}_defect.py', 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f'Generated: {filename}_defect.py')
        time.sleep(1)
        
    except Exception as e:
        print(f'Error {filename}: {e}')

print('Done!')
