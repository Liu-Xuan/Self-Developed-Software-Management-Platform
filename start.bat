@echo off
REM 激活虚拟环境
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo 创建虚拟环境...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
)

REM 设置环境变量
set FLASK_APP=run.py
set FLASK_ENV=development
set FLASK_DEBUG=1

REM 运行应用
python run.py --host=0.0.0.0 --port=5000 