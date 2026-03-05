import requests
import json

API_KEY = 'fuyi-kiro-17781158558'
API_URL = 'http://localhost:8000/v1/chat/completions'

tasks = [
    ('message_queue.py', 'MessageQueue', '消息队列系统：发布订阅、持久化、消费者组、ACK、重试'),
    ('email_service.py', 'EmailService', '邮件发送服务：SMTP连接、HTML/文本邮件、附件'),
    ('websocket_manager.py', 'WebSocketManager', 'WebSocket管理器：连接管理、心跳、断线重连'),
    ('sse_server.py', 'SSEManager', 'SSE推送服务：客户端管理、事件推送'),
    ('broadcaster.py', 'MessageBroadcaster', '消息广播：多通道订阅发布'),
    ('csv_exporter.py', 'CSVExporter', 'CSV导出：自定义列、编码、空值处理'),
    ('excel_parser.py', 'ExcelParser', 'Excel解析：xlsx读取、类型转换'),
    ('json_validator.py', 'JSONValidator', 'JSON验证：Schema校验、错误信息'),
    ('data_masker.py', 'DataMasker', '数据脱敏：手机号、邮箱、银行卡掩码'),
    ('data_encryptor.py', 'DataEncryptor', '数据加密：AES加密解密、密钥管理'),
]

results = []
for filename, classname, req in tasks:
    prompt = f'Python实现{classname}类：{req}。直接给完整代码，只回答代码'
    r = requests.post(API_URL, 
        headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
        json={'model': 'claude-sonnet-4.5', 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 8000})
    
    content = r.json()['choices'][0]['message']['content']
    # 提取代码部分
    if '```python' in content:
        code = content.split('```python')[1].split('```')[0]
    else:
        code = content
    
    # 保存到文件
    filepath = f'D:/_Progs/01Center/ODD/实证案例/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    
    results.append(f'Saved: {filename}')
    print(f'Generated: {filename}')

print('\\nDone!')
