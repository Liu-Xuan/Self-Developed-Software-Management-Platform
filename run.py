import os
import sys
import argparse
from app import app
from app.utils import PathHelper

def setup_environment():
    """设置运行环境"""
    # 获取脚本所在目录作为应用根目录
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        PathHelper.set_app_root(script_dir)
        os.chdir(script_dir)  # 切换工作目录
    except Exception as e:
        print(f"错误：无法设置工作目录: {str(e)}")
        sys.exit(1)
        
    # 确保必要的目录存在
    try:
        PathHelper.ensure_dir_exists(PathHelper.get_upload_dir())
        PathHelper.ensure_dir_exists(PathHelper.get_temp_dir())
    except Exception as e:
        print(f"错误：无法创建必要的目录: {str(e)}")
        sys.exit(1)
        
    # 设置环境变量
    os.environ['APP_ROOT'] = script_dir
    if 'FLASK_APP' not in os.environ:
        os.environ['FLASK_APP'] = 'run.py'

if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='运行Flask应用')
    parser.add_argument('--host', default='127.0.0.1', help='监听的主机地址')
    parser.add_argument('--port', type=int, default=5000, help='监听的端口')
    args = parser.parse_args()
    
    setup_environment()
    app.run(host=args.host, port=args.port, debug=True) 