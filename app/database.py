from app import db
from app.models import Software, File
from datetime import datetime

def init_db():
    """初始化数据库"""
    db.create_all()

def drop_db():
    """删除所有数据表"""
    db.drop_all()

def reset_db():
    """重置数据库（删除后重新创建）"""
    drop_db()
    init_db()

def update_software_status(software_id, status_type, value):
    """更新软件状态
    
    Args:
        software_id: 软件ID
        status_type: 状态类型 ('allow', 'install', 'release', 'receive')
        value: 状态值 (True/False)
    """
    software = Software.query.get(software_id)
    if software:
        status_field = f'status_{status_type}'
        if hasattr(software, status_field):
            setattr(software, status_field, value)
            db.session.commit()
            return True
    return False

def get_software_stats():
    """获取软件统计信息"""
    total = Software.query.count()
    stats = {
        'total': total,
        'by_type': {},
        'by_status': {
            'allow': Software.query.filter_by(status_allow=True).count(),
            'install': Software.query.filter_by(status_install=True).count(),
            'release': Software.query.filter_by(status_release=True).count(),
            'receive': Software.query.filter_by(status_receive=True).count()
        }
    }
    
    # 按类型统计
    for type_name in db.session.query(Software.type).distinct():
        if type_name[0]:  # 排除空类型
            count = Software.query.filter_by(type=type_name[0]).count()
            stats['by_type'][type_name[0]] = count
            
    return stats

def export_db_structure():
    """导出数据库结构"""
    structure = {}
    for table in db.metadata.tables.values():
        columns = {}
        for column in table.columns:
            columns[column.name] = {
                'type': str(column.type),
                'nullable': column.nullable,
                'primary_key': column.primary_key,
                'default': str(column.default) if column.default else None
            }
        structure[table.name] = columns
    return structure 