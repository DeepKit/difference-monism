
# csrf_protection.py
import secrets
import hashlib
from functools import wraps
from flask import Flask, session, request, abort, render_template_string

class CSRFProtection:
    """CSRF保护类"""
    
    def __init__(self, app=None, token_length=32):
        self.app = app
        self.token_length = token_length
        self.token_key = '_csrf_token'
        self.header_name = 'X-CSRF-Token'
        self.form_field = 'csrf_token'
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化Flask应用"""
        self.app = app
        app.config.setdefault('CSRF_ENABLED', True)
        app.config.setdefault('CSRF_TIME_LIMIT', 3600)
        
        # 注册模板全局函数
        app.jinja_env.globals['csrf_token'] = self.generate_token
        app.jinja_env.globals['csrf_input'] = self.csrf_input
        
        # 注册请求前钩子
        @app.before_request
        def csrf_protect():
            if not app.config.get('CSRF_ENABLED'):
                return
            
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                self.validate_token()
    
    def generate_token(self):
        """生成CSRF令牌"""
        if self.token_key not in session:
            session[self.token_key] = secrets.token_hex(self.token_length)
        return session[self.token_key]
    
    def validate_token(self):
        """验证CSRF令牌"""
        token = session.get(self.token_key)
        
        if not token:
            abort(403, description="CSRF令牌缺失")
        
        # 从请求中获取令牌
        request_token = None
        
        # 优先从header获取
        if self.header_name in request.headers:
            request_token = request.headers.get(self.header_name)
        # 其次从表单数据获取
        elif self.form_field in request.form:
            request_token = request.form.get(self.form_field)
        # 最后从JSON数据获取
        elif request.is_json and self.form_field in request.json:
            request_token = request.json.get(self.form_field)
        
        if not request_token:
            abort(403, description="CSRF令牌未提供")
        
        # 使用安全的比较方法
        if not secrets.compare_digest(token, request_token):
            abort(403, description="CSRF令牌无效")
    
    def csrf_input(self):
        """生成CSRF隐藏input标签"""
        token = self.generate_token()
        return f'<input type="hidden" name="{self.form_field}" value="{token}">'
    
    def exempt(self, view):
        """装饰器：豁免CSRF保护"""
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            return view(*args, **kwargs)
        wrapped_view._csrf_exempt = True
        return wrapped_view


def csrf_exempt(view):
    """独立的CSRF豁免装饰器"""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        return view(*args, **kwargs)
    wrapped_view._csrf_exempt = True
    return wrapped_view


# 使用示例
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# 初始化CSRF保护
csrf = CSRFProtection(app)

# 示例路由
@app.route('/')
def index():
    """显示表单页面"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CSRF保护示例</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>CSRF保护表单</h1>
        
        <!-- 普通表单提交 -->
        <form method="POST" action="/submit">
            {{ csrf_input()|safe }}
            <input type="text" name="data" placeholder="输入数据">
            <button type="submit">提交</button>
        </form>
        
        <hr>
        
        <!-- AJAX提交示例 -->
        <h2>AJAX提交</h2>
        <button onclick="submitAjax()">AJAX提交</button>
        
        <script>
        function submitAjax() {
            fetch('/api/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': '{{ csrf_token() }}'
                },
                body: JSON.stringify({data: 'test data'})
            })
            .then(response => response.json())
            .then(data => alert('成功: ' + JSON.stringify(data)))
            .catch(error => alert('错误: ' + error));
        }
        </script>
    </body>
    </html>
    '''
    return render_template_string(template)


@app.route('/submit', methods=['POST'])
def submit():
    """处理表单提交"""
    data = request.form.get('data')
    return f'<h1>提交成功</h1><p>数据: {data}</p><a href="/">返回</a>'


@app.route('/api/submit', methods=['POST'])
def api_submit():
    """处理API提交"""
    data = request.json.get('data')
    return {'status': 'success', 'data': data}


@app.route('/public', methods=['POST'])
@csrf_exempt
def public_endpoint():
    """公开端点，不需要CSRF保护"""
    return {'status': 'public endpoint'}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
