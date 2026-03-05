import requests

API_KEY = 'fuyi-kiro-17781158558'
API_URL = 'http://localhost:8000/v1/chat/completions'

tasks = [
    ('test_t036', 'memory_cache', 'MemoryCache', '内存缓存'),
    ('test_t037', 'disk_cache', 'DiskCache', '磁盘缓存'),
    ('test_t038', 'multi_level_cache', 'MultiLevelCache', '多级缓存'),
    ('test_t039', 'cache_warming', 'CacheWarming', '缓存预热'),
    ('test_t040', 'cache_invalidation', 'CacheInvalidation', '缓存失效'),
    ('test_t041', 'jwt_token', 'JWTTokenManager', 'JWT令牌'),
    ('test_t042', 'api_signature', 'APISignatureValidator', 'API签名'),
    ('test_t043', 'rate_limiter_v2', 'RequestRateLimiter', '请求限流'),
    ('test_t044', 'csrf_protector', 'CSRFProtector', 'CSRF防护'),
    ('test_t045', 'xss_filter', 'XSSFilter', 'XSS过滤'),
    ('test_t046', 'order_state_machine', 'OrderStateMachine', '订单状态机'),
    ('test_t047', 'workflow_engine', 'WorkflowEngine', '工作流引擎'),
    ('test_t048', 'rules_engine', 'RulesEngine', '规则引擎'),
    ('test_t049', 'metrics_calculator', 'BusinessMetricsCalculator', '业务指标'),
    ('test_t050', 'report_generator', 'ReportGenerator', '报表生成'),
]

for test_file, module, classname, name in tasks:
    prompt = f'pytest测试用例：测试{classname}类。基本功能测试'
    
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
