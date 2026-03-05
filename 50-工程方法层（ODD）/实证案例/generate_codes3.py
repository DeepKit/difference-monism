import requests

API_KEY = 'fuyi-kiro-17781158558'
API_URL = 'http://localhost:8000/v1/chat/completions'

tasks = [
    ('memory_cache.py', 'MemoryCache', '内存缓存：TTL过期、LRU淘汰、容量限制'),
    ('disk_cache.py', 'DiskCache', '磁盘缓存：持久化、自动清理、序列化'),
    ('multi_level_cache.py', 'MultiLevelCache', '多级缓存：L1/L2级联、缓存穿透保护'),
    ('cache_warming.py', 'CacheWarming', '缓存预热：启动预加载、异步预热'),
    ('cache_invalidation.py', 'CacheInvalidation', '缓存失效：主动失效、延迟失效、订阅失效'),
    ('jwt_token.py', 'JWTTokenManager', 'JWT令牌管理：生成、验证、刷新'),
    ('api_signature.py', 'APISignatureValidator', 'API签名验证：HMAC-SHA256、时间戳防重放'),
    ('rate_limiter_v2.py', 'RequestRateLimiter', '请求限流：令牌桶、滑窗计数'),
    ('csrf_protector.py', 'CSRFProtector', 'CSRF防护：Token生成、验证'),
    ('xss_filter.py', 'XSSFilter', 'XSS过滤：HTML转义、脚本过滤'),
    ('order_state_machine.py', 'OrderStateMachine', '订单状态机：状态流转、事件触发'),
    ('workflow_engine.py', 'WorkflowEngine', '工作流引擎：节点编排、条件分支'),
    ('rules_engine.py', 'RulesEngine', '规则引擎：条件匹配、动作执行'),
    ('metrics_calculator.py', 'BusinessMetricsCalculator', '业务指标计算：PV/UV、转化率'),
    ('report_generator.py', 'ReportGenerator', '报表生成：多维度统计、导出PDF/Excel'),
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