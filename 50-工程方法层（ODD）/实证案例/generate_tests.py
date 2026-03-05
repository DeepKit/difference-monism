import requests

API_KEY = 'fuyi-kiro-17781158558'
API_URL = 'http://localhost:8000/v1/chat/completions'

tasks = [
    ('test_t016', 'message_queue', 'MessageQueue', '消息队列'),
    ('test_t017', 'email_service', 'EmailService', '邮件服务'),
    ('test_t018', 'websocket_manager', 'WebSocketManager', 'WebSocket'),
    ('test_t019', 'sse_server', 'SSEManager', 'SSE推送'),
    ('test_t020', 'broadcaster', 'MessageBroadcaster', '消息广播'),
    ('test_t021', 'csv_exporter', 'CSVExporter', 'CSV导出'),
    ('test_t022', 'excel_parser', 'ExcelParser', 'Excel解析'),
    ('test_t023', 'json_validator', 'JSONValidator', 'JSON验证'),
    ('test_t024', 'data_masker', 'DataMasker', '数据脱敏'),
    ('test_t025', 'data_encryptor', 'DataEncryptor', '数据加密'),
]

results = []
for test_file, module, classname, name in tasks:
    prompt = f'''pytest测试用例：测试{classname}类
包含基本功能测试：
1. 初始化测试
2. 核心方法测试
3. 边界情况测试

直接给完整pytest代码，只需要能运行的测试用例'''
    
    r = requests.post(API_URL, 
        headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
        json={'model': 'claude-sonnet-4.5', 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 6000})
    
    content = r.json()['choices'][0]['message']['content']
    if '```python' in content:
        code = content.split('```python')[1].split('```')[0]
    else:
        code = content
    
    # 修复import
    code = code.replace('from ' + module + ' import', f'from ' + module + ' import')
    
    filepath = f'D:/_Progs/01Center/ODD/实证案例/{test_file}.py'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f'Generated: {test_file}.py')

print('\nDone!')
