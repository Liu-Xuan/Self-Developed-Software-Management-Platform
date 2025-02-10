#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
else
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "安装依赖包..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "警告: 未找到requirements.txt文件"
    fi
fi

# 设置环境变量
export FLASK_APP=run.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export APP_ROOT="$SCRIPT_DIR"

# 检查必要文件
if [ ! -f "run.py" ]; then
    echo "错误: 未找到run.py文件"
    exit 1
fi

# 初始化数据库
echo "初始化数据库..."
if [ -f "app.db" ]; then
    echo "数据库文件已存在，跳过初始化"
else
    echo "创建数据库表结构..."
    flask db upgrade || {
        echo "创建数据库失败，尝试重新初始化..."
        rm -f app.db
        flask db init
        flask db migrate -m "initial migration"
        flask db upgrade
    }
fi

echo "启动应用..."
# 运行应用
python run.py 