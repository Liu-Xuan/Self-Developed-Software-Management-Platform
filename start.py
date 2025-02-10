from waitress import serve
from app import app

if __name__ == '__main__':
    # 使用waitress作为生产环境服务器
    # host='0.0.0.0'表示允许所有IP访问
    # port=8080为服务端口号，可根据需要修改
    print("Starting server on http://0.0.0.0:8080")
    serve(app, host='0.0.0.0', port=8080, threads=4) 