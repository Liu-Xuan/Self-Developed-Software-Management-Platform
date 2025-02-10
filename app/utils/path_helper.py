import os
import sys
from typing import Optional

class PathHelper:
    """跨平台路径处理工具类
    
    用于处理不同操作系统下的文件路径，确保路径的一致性和兼容性
    """
    
    _app_root = None
    
    @staticmethod
    def get_app_root() -> str:
        """获取应用程序根目录"""
        if PathHelper._app_root is None:
            # 尝试从当前文件位置获取
            try:
                PathHelper._app_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            except:
                # 如果失败，尝试从环境变量获取
                PathHelper._app_root = os.environ.get('APP_ROOT')
                if not PathHelper._app_root:
                    # 如果环境变量也没有，使用当前工作目录
                    try:
                        PathHelper._app_root = os.getcwd()
                    except:
                        raise RuntimeError("无法确定应用程序根目录")
                        
        return PathHelper._app_root
        
    @staticmethod
    def set_app_root(path: str) -> None:
        """设置应用程序根目录
        
        Args:
            path: 根目录路径
        """
        if os.path.exists(path):
            PathHelper._app_root = path
        else:
            raise ValueError(f"指定的路径不存在: {path}")
        
    @staticmethod
    def ensure_app_root() -> None:
        """确保应用程序根目录已设置且存在"""
        root = PathHelper.get_app_root()
        if not os.path.exists(root):
            raise RuntimeError(f"应用程序根目录不存在: {root}")
        
    @staticmethod
    def get_upload_dir() -> str:
        """获取上传文件目录"""
        upload_dir = os.path.join(PathHelper.get_app_root(), 'uploads')
        PathHelper.ensure_dir_exists(upload_dir)
        return upload_dir
        
    @staticmethod
    def get_temp_dir() -> str:
        """获取临时文件目录"""
        temp_dir = os.path.join(PathHelper.get_app_root(), 'temp')
        PathHelper.ensure_dir_exists(temp_dir)
        return temp_dir
        
    @staticmethod
    def get_static_dir() -> str:
        """获取静态文件目录"""
        return os.path.join(PathHelper.get_app_root(), 'app', 'static')
        
    @staticmethod
    def get_template_dir() -> str:
        """获取模板文件目录"""
        return os.path.join(PathHelper.get_app_root(), 'app', 'templates')
        
    @staticmethod
    def normalize_path(path: str) -> str:
        """标准化文件路径
        
        将路径转换为当前操作系统的标准格式
        
        Args:
            path: 原始路径
            
        Returns:
            标准化后的路径
        """
        return os.path.normpath(path)
        
    @staticmethod
    def ensure_dir_exists(dir_path: str) -> None:
        """确保目录存在
        
        如果目录不存在则创建
        
        Args:
            dir_path: 目录路径
        """
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
    @staticmethod
    def get_system_fonts_dir() -> Optional[str]:
        """获取系统字体目录
        
        Returns:
            系统字体目录路径，如果不存在返回None
        """
        if sys.platform == 'win32':
            return os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Fonts')
        elif sys.platform == 'darwin':  # macOS
            return '/System/Library/Fonts'
        elif sys.platform.startswith('linux'):
            return '/usr/share/fonts'
        return None 