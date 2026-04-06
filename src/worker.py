import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vendor'))

# 延迟初始化
app = None

def get_app():
    global app
    if app is None:
        from flask import Flask, request, jsonify
        app = Flask(__name__)
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        
        @app.route('/')
        def hello():
            return jsonify({"message": "Hello from Flask on Cloudflare Workers!", "status": "ok"})
        
        @app.route('/health')
        def health():
            return "OK", 200
        
        # 禁用 Jinja2
        app.jinja_env = None
        app.jinja_loader = None
    return app


async def on_fetch(request, env):
    # 将环境变量注入
    for key, value in env.__dict__.items():
        os.environ[key] = str(value)
    
    # 获取或创建应用
    flask_app = get_app()
    
    # 构建 WSGI 环境（同之前）
    environ = {
        'REQUEST_METHOD': request.method,
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query_string.decode('utf-8') if request.query_string else '',
        'SERVER_NAME': 'cloudflare-worker',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': request.body or b'',
        'wsgi.errors': None,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': True,
    }
    
    for key, value in request.headers.items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    if 'CONTENT_TYPE' not in environ and 'Content-Type' in request.headers:
        environ['CONTENT_TYPE'] = request.headers['Content-Type']
    
    if request.body:
        environ['CONTENT_LENGTH'] = str(len(request.body))
    
    response_data = []
    def start_response(status, headers):
        response_data.extend([status, headers])
    
    result = flask_app.wsgi_app(environ, start_response)
    status_code = int(response_data[0].split()[0])
    headers = response_data[1]
    body = b''.join(result)
    
    from js import Response as JsResponse
    return JsResponse.new(body, status=status_code, headers=dict(headers))