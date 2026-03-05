
from flask import Flask, Response, render_template_string
import time
import json
from datetime import datetime
from queue import Queue
import threading

app = Flask(__name__)

# 存储所有活跃的客户端连接
clients = []
clients_lock = threading.Lock()

# HTML客户端页面（可选，用于测试）
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SSE Client</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Server-Sent Events Demo</h1>
    <div id="messages"></div>
    <script>
        const eventSource = new EventSource('/stream');
        const messagesDiv = document.getElementById('messages');
        
        eventSource.onmessage = function(event) {
            const p = document.createElement('p');
            p.textContent = 'Message: ' + event.data;
            messagesDiv.appendChild(p);
        };
        
        eventSource.addEventListener('custom', function(event) {
            const p = document.createElement('p');
            p.textContent = 'Custom Event: ' + event.data;
            p.style.color = 'blue';
            messagesDiv.appendChild(p);
        });
        
        eventSource.onerror = function(error) {
            console.error('SSE Error:', error);
        };
    </script>
</body>
</html>
"""

def event_stream():
    """生成SSE事件流"""
    queue = Queue()
    
    with clients_lock:
        clients.append(queue)
    
    try:
        while True:
            # 从队列获取消息
            message = queue.get()
            
            if message is None:
                break
                
            yield message
    finally:
        with clients_lock:
            clients.remove(queue)

def format_sse(data, event=None, id=None, retry=None):
    """格式化SSE消息"""
    message = ''
    
    if event:
        message += f'event: {event}\n'
    
    if id:
        message += f'id: {id}\n'
    
    if retry:
        message += f'retry: {retry}\n'
    
    # 处理多行数据
    if isinstance(data, dict):
        data = json.dumps(data)
    
    for line in str(data).split('\n'):
        message += f'data: {line}\n'
    
    message += '\n'
    return message

def broadcast_message(data, event=None, id=None):
    """向所有客户端广播消息"""
    message = format_sse(data, event=event, id=id)
    
    with clients_lock:
        for client_queue in clients:
            try:
                client_queue.put(message)
            except:
                pass

@app.route('/')
def index():
    """返回测试页面"""
    return render_template_string(HTML_PAGE)

@app.route('/stream')
def stream():
    """SSE端点"""
    return Response(
        event_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )

@app.route('/send/<message>')
def send_message(message):
    """手动发送消息的API端点"""
    broadcast_message(message)
    return {'status': 'sent', 'message': message}

@app.route('/send_custom/<message>')
def send_custom(message):
    """发送自定义事件"""
    broadcast_message(message, event='custom')
    return {'status': 'sent', 'event': 'custom', 'message': message}

def background_task():
    """后台任务：定期发送消息"""
    counter = 0
    while True:
        time.sleep(5)
        counter += 1
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'counter': counter,
            'message': f'自动消息 #{counter}'
        }
        
        broadcast_message(data, id=str(counter))

if __name__ == '__main__':
    # 启动后台任务线程
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()
    
    # 启动Flask服务器
    app.run(host='0.0.0.0', port=5000, threaded=True)
