from app import app, db
from app.models import Software
from datetime import datetime, UTC

def import_initial_data():
    """导入初始数据到数据库"""
    
    # 初始数据
    initial_data = [
        {
            'type': 'ORT',
            'name': '23 SDU USER ORT',
            'model': 'B777-300ER',
            'partnumber': '2300-CCA-USE-21',
            'status_allow': True,
            'status_install': True,
            'vendor': '',  # 空值
            'mediapn': '',  # 空值
            'description': '',  # 空值
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SDU USER ORT',
            'model': 'B737-8',
            'partnumber': '2308-BEJ-USE-07',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SDU USER ORT',
            'model': 'B737NG',
            'partnumber': '2309-BEJ-USE-06',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SDU USER ORT',
            'model': 'B737-8',
            'partnumber': '2375-BCG-U00-R5',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SATCOM USER ORT',
            'model': 'B747-400',
            'partnumber': '747-USERORT-RS',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SATCOM USER ORT',
            'model': 'A319',
            'partnumber': 'CCA-A319-035',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SATCOM USER ORT',
            'model': 'A319',
            'partnumber': 'CCA-A319-080',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SDU USER ORT',
            'model': 'B747-8',
            'partnumber': 'CCA43-SATC-0016',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SDU USER ORT',
            'model': 'B747-8',
            'partnumber': 'CCA44-SATC-7016',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SATCOM USER ORT',
            'model': 'B747-400',
            'partnumber': 'CCA52-USER-0002',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        },
        {
            'type': 'ORT',
            'name': '23 SATCOM USER ORT',
            'model': 'A319',
            'partnumber': 'CSC524501002300',
            'status_allow': True,
            'status_install': True,
            'vendor': '',
            'mediapn': '',
            'description': '',
            'creator': '系统导入',
            'release_date': datetime.now(UTC)
        }
    ]
    
    try:
        # 清空现有数据
        Software.query.delete()
        
        # 添加新数据
        for data in initial_data:
            software = Software(**data)
            db.session.add(software)
        
        # 提交事务
        db.session.commit()
        print("数据导入成功！")
        
    except Exception as e:
        db.session.rollback()
        print(f"数据导入失败：{str(e)}")
        raise

if __name__ == '__main__':
    with app.app_context():
        import_initial_data() 