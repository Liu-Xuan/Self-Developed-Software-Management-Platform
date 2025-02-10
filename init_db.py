from app import app, db
from app.database import init_db

if __name__ == '__main__':
    with app.app_context():
        init_db()
        print("数据库初始化完成！") 