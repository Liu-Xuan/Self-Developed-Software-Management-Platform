import click
from flask.cli import with_appcontext
from app import app, db
from app.models import Software, File
from app.database import init_db, drop_db, reset_db, export_db_structure, get_software_stats
import json
from datetime import datetime

@app.cli.command('init-db')
@with_appcontext
def init_db_command():
    """初始化数据库"""
    init_db()
    click.echo('数据库初始化完成。')

@app.cli.command('drop-db')
@with_appcontext
def drop_db_command():
    """删除数据库"""
    if click.confirm('此操作将删除所有数据，是否继续？'):
        drop_db()
        click.echo('数据库已删除。')

@app.cli.command('reset-db')
@with_appcontext
def reset_db_command():
    """重置数据库"""
    if click.confirm('此操作将删除所有数据并重新创建数据库，是否继续？'):
        reset_db()
        click.echo('数据库已重置。')

@app.cli.command('show-structure')
@with_appcontext
def show_structure_command():
    """显示数据库结构"""
    structure = export_db_structure()
    click.echo(json.dumps(structure, indent=2, ensure_ascii=False))

@app.cli.command('show-stats')
@with_appcontext
def show_stats_command():
    """显示数据统计信息"""
    stats = get_software_stats()
    click.echo(json.dumps(stats, indent=2, ensure_ascii=False))

@app.cli.command('update-status')
@click.argument('software_id', type=int)
@click.argument('status_type', type=click.Choice(['allow', 'install', 'release', 'receive']))
@click.argument('value', type=bool)
@with_appcontext
def update_status_command(software_id, status_type, value):
    """更新软件状态"""
    software = Software.query.get(software_id)
    if software:
        status_field = f'status_{status_type}'
        if hasattr(software, status_field):
            setattr(software, status_field, value)
            db.session.commit()
            click.echo(f'软件 {software.name} 的 {status_type} 状态已更新为 {value}')
        else:
            click.echo(f'无效的状态类型：{status_type}')
    else:
        click.echo(f'未找到ID为 {software_id} 的软件')

@app.cli.command('list-software')
@with_appcontext
def list_software_command():
    """列出所有软件"""
    softwares = Software.query.all()
    for software in softwares:
        click.echo(f"""
ID: {software.id}
名称: {software.name}
类型: {software.type}
版本: {software.version}
机型: {software.model or '-'}
厂家: {software.vendor or '-'}
状态: 允装={software.status_allow}, 实装={software.status_install}, 
     发布={software.status_release}, 接收={software.status_receive}
发布日期: {software.release_date.strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 50}""") 