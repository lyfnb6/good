// worker.js - Cloudflare Worker 入口文件
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // 处理 favicon.ico 请求
    if (path === '/favicon.ico') {
      return new Response(null, { status: 204 });
    }

    // 处理根路径请求 - 返回 HTML 页面
    if (path === '/') {
      const html = `<!DOCTYPE html>
      <html lang="zh-CN">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>我的网站</title>
          <style>
              body {
                  font-family: system-ui, -apple-system, sans-serif;
                  text-align: center;
                  padding: 50px;
                  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                  color: white;
                  min-height: 100vh;
                  margin: 0;
                  display: flex;
                  justify-content: center;
                  align-items: center;
              }
              .card {
                  background: rgba(255,255,255,0.1);
                  backdrop-filter: blur(10px);
                  border-radius: 20px;
                  padding: 40px;
                  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
              }
              h1 { font-size: 2.5em; margin-bottom: 20px; }
              p { font-size: 1.2em; line-height: 1.6; opacity: 0.9; }
              button {
                  background: white;
                  color: #667eea;
                  border: none;
                  padding: 12px 30px;
                  font-size: 1em;
                  border-radius: 30px;
                  cursor: pointer;
                  margin-top: 20px;
                  font-weight: bold;
              }
              button:hover {
                  transform: scale(1.05);
                  transition: transform 0.3s;
              }
          </style>
      </head>
      <body>
          <div class="card">
              <h1>🎉 部署成功！</h1>
              <p>你的 Cloudflare Worker 正在通过 JavaScript 稳定运行</p>
              <p>之前的 Python 兼容性问题已经彻底解决</p>
              <button onclick="alert('Hello from Worker!')">点击测试</button>
          </div>
      </body>
      </html>`;
      
      return new Response(html, {
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
      });
    }

    // 处理 API 请求示例
    if (path === '/api/hello') {
      const data = { message: 'Hello from Worker API!', timestamp: Date.now() };
      return new Response(JSON.stringify(data), {
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // 404 处理
    return new Response('Page Not Found', { status: 404 });
  },
};