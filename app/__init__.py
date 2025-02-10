from flask import Flask
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