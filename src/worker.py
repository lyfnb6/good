import sys
import os

# 将 vendor 目录添加到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vendor'))

from flask import Flask, request, jsonify

# 创建 Flask 应用
app = Flask(__name__)

# 禁用模板引擎以节省资源
app.jinja_env = None
app.jinja_loader = None

# 精简配置
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = False


@app.route('/')
def hello():
    return jsonify({"message": "Hello from Flask on Cloudflare Workers!", "status": "ok"})


@app.route('/health')
def health():
    return "OK", 200


@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({"echo": data, "method": request.method})


async def on_fetch(request, env):
    """Cloudflare Worker 入口函数"""
    # 注入环境变量
    for key, value in env.__dict__.items():
        os.environ[key] = str(value)
    
    # 构建 WSGI 环境
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
    
    # 添加请求头
    for key, value in request.headers.items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
    
    # 添加 Content-Type
    if 'CONTENT_TYPE' not in environ and 'Content-Type' in request.headers:
        environ['CONTENT_TYPE'] = request.headers['Content-Type']
    
    # 添加 Content-Length
    if request.body:
        environ['CONTENT_LENGTH'] = str(len(request.body))
    
    # 调用 Flask
    response_data = []
    def start_response(status, headers):
        response_data.extend([status, headers])
    
    result = app.wsgi_app(environ, start_response)
    status_code = int(response_data[0].split()[0])
    headers = response_data[1]
    body = b''.join(result)
    
    # 构建响应
    from js import Response as JsResponse
    return JsResponse.new(body, status=status_code, headers=dict(headers))