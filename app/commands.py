from flask.cli import with_appcontext
import click
from app import db
from app.models import Software, ProcessDocument

@click.command('init-docs')
@with_appcontext
def init_docs_command():
    """初始化流程文档数据"""
    # ORT通用文档
    ort_general = ProcessDocument(
        type='ORT',
        doc_type='general',
        title='ORT软件通用指南',
        content="""
<div class="process-doc">
    <h4>ORT软件通用指南</h4>
    
    <div class="section">
        <h5>1. 软件概述</h5>
        <ul>
            <li>ORT软件定义和用途</li>
            <li>软件架构和组成
                <ul>
                    <li>核心模块</li>
                    <li>功能模块</li>
                    <li>接口模块</li>
                </ul>
            </li>
        </ul>
    </div>
    
    <div class="section">
        <h5>2. 基本要求</h5>
        <ul>
            <li>开发环境要求</li>
            <li>运行环境要求</li>
            <li>性能要求</li>
            <li>安全要求</li>
        </ul>
    </div>
    
    <div class="alert alert-info">
        <h5>相关资源</h5>
        <ul>
            <li><a href="#" target="_blank">ORT软件规范文档</a></li>
            <li><a href="#" target="_blank">环境配置指南</a></li>
        </ul>
    </div>
</div>
"""
    )
    
    # ORT开发指南
    ort_dev = ProcessDocument(
        type='ORT',
        doc_type='development',
        title='ORT软件开发指南',
        content="""
<div class="process-doc">
    <h4>ORT软件开发指南</h4>
    
    <div class="section">
        <h5>1. 开发流程</h5>
        <ol>
            <li>需求分析</li>
            <li>概要设计</li>
            <li>详细设计</li>
            <li>编码实现</li>
            <li>单元测试</li>
            <li>集成测试</li>
        </ol>
    </div>
    
    <div class="section">
        <h5>2. 开发规范</h5>
        <ul>
            <li>代码规范</li>
            <li>注释规范</li>
            <li>命名规范</li>
            <li>版本控制规范</li>
        </ul>
    </div>
    
    <div class="alert alert-info">
        <h5>开发工具</h5>
        <ul>
            <li><a href="#" class="tool-link">开发环境配置工具</a></li>
            <li><a href="#" class="tool-link">代码检查工具</a></li>
        </ul>
    </div>
</div>
"""
    )
    
    # ACMS通用文档
    acms_general = ProcessDocument(
        type='ACMS',
        doc_type='general',
        title='ACMS软件通用指南',
        content="""
<div class="process-doc">
    <h4>ACMS软件通用指南</h4>
    
    <div class="section">
        <h5>1. 软件概述</h5>
        <ul>
            <li>ACMS软件定义和用途</li>
            <li>系统架构
                <ul>
                    <li>数据库设计</li>
                    <li>业务逻辑</li>
                    <li>用户界面</li>
                </ul>
            </li>
        </ul>
    </div>
    
    <div class="section">
        <h5>2. 基本要求</h5>
        <ul>
            <li>系统要求</li>
            <li>性能指标</li>
            <li>安全规范</li>
            <li>接口标准</li>
        </ul>
    </div>
    
    <div class="alert alert-info">
        <h5>相关资源</h5>
        <ul>
            <li><a href="#" target="_blank">ACMS系统文档</a></li>
            <li><a href="#" target="_blank">数据库设计规范</a></li>
        </ul>
    </div>
</div>
"""
    )
    
    # ACMS开发指南
    acms_dev = ProcessDocument(
        type='ACMS',
        doc_type='development',
        title='ACMS软件开发指南',
        content="""
<div class="process-doc">
    <h4>ACMS软件开发指南</h4>
    
    <div class="section">
        <h5>1. 开发流程</h5>
        <ol>
            <li>数据库设计</li>
            <li>接口设计</li>
            <li>业务逻辑实现</li>
            <li>界面开发</li>
            <li>单元测试</li>
            <li>集成测试</li>
        </ol>
    </div>
    
    <div class="section">
        <h5>2. 开发规范</h5>
        <ul>
            <li>数据库规范</li>
            <li>代码规范</li>
            <li>接口规范</li>
            <li>UI设计规范</li>
        </ul>
    </div>
    
    <div class="alert alert-info">
        <h5>开发工具</h5>
        <ul>
            <li><a href="#" class="tool-link">数据库管理工具</a></li>
            <li><a href="#" class="tool-link">接口测试工具</a></li>
        </ul>
    </div>
</div>
"""
    )
    
    # 添加所有文档
    docs = [ort_general, ort_dev, acms_general, acms_dev]
    for doc in docs:
        db.session.add(doc)
    
    db.session.commit()
    click.echo('流程文档初始化完成')

def init_app(app):
    """注册自定义命令"""
    app.cli.add_command(init_docs_command) 