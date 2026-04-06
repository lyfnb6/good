from flask import Flask, request, jsonify

app = Flask(__name__)

# 精简配置
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = False


@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Flask on Cloudflare Workers!",
        "status": "ok"
    })


@app.route('/health')
def health():
    return "OK", 200


@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({
        "echo": data,
        "method": request.method
    })


# 本地开发测试
if __name__ == '__main__':
    app.run(debug=True, port=5000)