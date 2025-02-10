import os
import sys

def ensure_windows_compatibility():
    """确保Windows系统兼容性的配置函数"""
    
    # 设置文件编码
    if sys.platform == 'win32':
        import locale
        sys.stdout.reconfigure(encoding=locale.getpreferredencoding())
    
    # 确保上传目录存在
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    if not os.path.exists(upload_dir):
        try:
            os.makedirs(upload_dir)
        except Exception as e:
            print(f"创建上传目录失败: {str(e)}")
            
    # 设置临时文件目录
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
    if not os.path.exists(temp_dir):
        try:
            os.makedirs(temp_dir)
        except Exception as e:
            print(f"创建临时目录失败: {str(e)}")
            
    return {
        'upload_dir': upload_dir,
        'temp_dir': temp_dir
    } 