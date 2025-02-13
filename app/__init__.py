from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import sys

# 初始化Flask应用
app = Flask(__name__)
app.config.from_object(Config)

# Windows系统特定配置
if sys.platform == 'win32':
    from win_config import ensure_windows_compatibility
    win_config = ensure_windows_compatibility()
    app.config['UPLOAD_FOLDER'] = win_config['upload_dir']
    app.config['TEMP_FOLDER'] = win_config['temp_dir']

# 初始化数据库
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 导入路由和模型（移到最后以避免循环导入）
from app import routes, models, commands
commands.init_app(app)  # 注册自定义命令

@app.after_request
def add_security_headers(response):
    """添加安全性和缓存控制头"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # 根据文件类型设置正确的Content-Type
    if request.path.endswith('.css'):
        response.headers['Content-Type'] = 'text/css; charset=utf-8'
    else:
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
    
    # 对静态资源添加缓存控制
    if request.path.startswith(('/static/', '/docs/')):
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    else:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    
    return response

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Windows系统特定配置
    if sys.platform == 'win32':
        from win_config import ensure_windows_compatibility
        win_config = ensure_windows_compatibility()
        app.config['UPLOAD_FOLDER'] = win_config['upload_dir']
        app.config['TEMP_FOLDER'] = win_config['temp_dir']
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    return app 