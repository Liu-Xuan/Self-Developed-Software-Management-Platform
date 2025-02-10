import os
from datetime import timedelta
from app.utils import PathHelper

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(PathHelper.get_app_root(), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 限制上传文件大小为100MB
    UPLOAD_FOLDER = PathHelper.get_upload_dir()
    TEMP_FOLDER = PathHelper.get_temp_dir()
    
    # 确保目录存在
    PathHelper.ensure_dir_exists(UPLOAD_FOLDER)
    PathHelper.ensure_dir_exists(TEMP_FOLDER)
    
    # Session配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # 调试工具栏（仅在开发环境启用）
    DEBUG_TB_ENABLED = os.environ.get('FLASK_ENV') == 'development'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    # 文件上传配置
    ALLOWED_EXTENSIONS = {'zip', 'rar', '7z'} 