from datetime import datetime
from app import db
from sqlalchemy import and_, or_

class Software(db.Model):
    """软件信息表"""
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))                   # 软件类型
    model = db.Column(db.String(50))                  # 适用机型
    vendor = db.Column(db.String(100))                # 厂家
    name = db.Column(db.String(100), nullable=False)  # 软件名称
    partnumber = db.Column(db.String(20), nullable=False)# 软件件号
    mediapn = db.Column(db.String(20), nullable=False)# 媒体集号
    description = db.Column(db.Text)                  # 描述
    creator = db.Column(db.String(50), default='匿名') # 创建者
    release_date = db.Column(db.DateTime, default=datetime.utcnow)  # 发布日期
    
    # 状态字段
    status_allow = db.Column(db.Boolean, default=False)     # 允装状态
    status_install = db.Column(db.Boolean, default=False)   # 实装状态
    status_release = db.Column(db.Boolean, default=False)   # 发布状态
    status_receive = db.Column(db.Boolean, default=False)   # 接收状态
    
    files = db.relationship('File', backref='software', lazy=True)

    def __repr__(self):
        return f'<Software {self.name} {self.partnumber}>'
    
    @classmethod
    def get_latest_versions(cls):
        """获取每个软件（相同类型+机型+厂家+名称）的最新版本，且状态为允装或实装的记录"""
        # 子查询：获取每组软件的最新发布日期
        latest_dates = db.session.query(
            cls.type,
            cls.model,
            cls.vendor,
            cls.name,
            db.func.max(cls.release_date).label('max_date')
        ).group_by(
            cls.type,
            cls.model,
            cls.vendor,
            cls.name
        ).subquery()
        
        # 主查询：获取最新的软件记录，并且状态为允装或实装
        return cls.query.join(
            latest_dates,
            and_(
                cls.type == latest_dates.c.type,
                cls.model == latest_dates.c.model,
                cls.vendor == latest_dates.c.vendor,
                cls.name == latest_dates.c.name,
                cls.release_date == latest_dates.c.max_date
            )
        ).filter(
            or_(
                cls.status_allow == True,
                cls.status_install == True
            )
        ).order_by(
            cls.type,
            cls.model,
            cls.vendor,
            cls.name,
            cls.release_date.desc()
        ).all()

class ProcessDocument(db.Model):
    """软件制作流程文档表"""
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))                   # 软件类型 (ORT/ACMS)
    doc_type = db.Column(db.String(50))              # 文档类型 (general/development/test/release)
    model = db.Column(db.String(50))                  # 适用机型（可选）
    vendor = db.Column(db.String(100))                # 厂家（可选）
    title = db.Column(db.String(200), nullable=False) # 文档标题
    content = db.Column(db.Text, nullable=False)      # 文档内容（支持HTML格式）
    create_time = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间

    def __repr__(self):
        return f'<ProcessDocument {self.title}>'

class File(db.Model):
    """文件存储表"""
    id = db.Column(db.Integer, primary_key=True)
    software_id = db.Column(db.Integer, db.ForeignKey('software.id'), nullable=False)
    file_path = db.Column(db.String(255), unique=True)  # 文件存储路径
    original_filename = db.Column(db.String(255), nullable=False)  # 原始文件名
    coc_path = db.Column(db.String(255))               # COC文档路径
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)  # 上传时间

    def __repr__(self):
        return f'<File {self.original_filename}>' 