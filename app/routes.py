import os
from flask import render_template, request, redirect, url_for, flash, current_app, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Software, File, ProcessDocument, SystemLog
from app.utils import PDFTemplate
from app.utils.markdown_processor import MarkdownProcessor
from datetime import datetime
from app.utils.html_processor import process_html_file

# 系统管理密码（后续会替换为权限管理模块）
ADMIN_PASSWORD = "admin123"

def allowed_file(filename):
    """检查文件类型是否允许"""
    ALLOWED_EXTENSIONS = {'zip', 'rar', '7z', 'tar', 'gz'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    """生成唯一的文件名"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(original_filename)
    return f"{name}_{timestamp}{ext}"

def generate_coc_pdf(software, save_path, template_path=None):
    """生成软件COC PDF文档
    
    Args:
        software: 软件对象
        save_path: PDF保存路径
        template_path: 可选的模板文件路径
    """
    # 准备数据
    data = {
        'type': software.type,
        'model': software.model or '',
        'vendor': software.vendor or '',
        'name': software.name,
        'partnumber': software.partnumber,
        'mediapn': software.mediapn or '',
        'description': software.description or '',
        'creator': software.creator or '系统',
        'release_date': software.release_date.strftime('%Y-%m-%d %H:%M:%S') if software.release_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status_allow': software.status_allow,
        'status_install': software.status_install,
        'status_release': software.status_release,
        'status_receive': software.status_receive
    }
    
    # 使用模板生成PDF
    pdf_template = PDFTemplate()
    if template_path:
        pdf_template.load_template(template_path)
    pdf_template.generate(data, save_path)

def log_operation(operation, description, operator="系统"):
    """记录系统操作日志"""
    log = SystemLog(
        operation=operation,
        description=description,
        operator=operator,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

@app.route('/')
def index():
    """主页：显示软件列表"""
    # 获取筛选参数
    type_filter = request.args.get('type')
    model_filter = request.args.get('model')
    vendor_filter = request.args.get('vendor')
    
    # 获取状态筛选参数
    status_allow = request.args.get('status_allow')
    status_install = request.args.get('status_install')
    status_release = request.args.get('status_release')
    status_receive = request.args.get('status_receive')
    
    # 获取排序参数
    sort_by = request.args.get('sort', 'type')  # 默认按类型排序
    sort_order = request.args.get('order', 'asc')  # 默认升序
    
    # 获取所有唯一值用于筛选
    types = db.session.query(Software.type).distinct().all()
    models = db.session.query(Software.model).distinct().all()
    vendors = db.session.query(Software.vendor).distinct().all()
    
    # 构建基础查询
    query = Software.query
    
    # 应用筛选条件
    if type_filter:
        query = query.filter(Software.type == type_filter)
    if model_filter:
        query = query.filter(Software.model == model_filter)
    if vendor_filter:
        query = query.filter(Software.vendor == vendor_filter)
        
    # 应用状态筛选
    if status_allow:
        query = query.filter(Software.status_allow == True)
    if status_install:
        query = query.filter(Software.status_install == True)
    if status_release:
        query = query.filter(Software.status_release == True)
    if status_receive:
        query = query.filter(Software.status_receive == True)
    
    # 应用排序
    sort_column = getattr(Software, sort_by)
    if sort_order == 'desc':
        sort_column = sort_column.desc()
    
    # 默认的多列排序
    query = query.order_by(
        sort_column,
        Software.type,
        Software.model,
        Software.vendor,
        Software.release_date.desc()
    )
    
    # 获取软件列表
    softwares = query.all()
    
    return render_template('index.html', 
                         softwares=softwares,
                         types=[t[0] for t in types if t[0]],
                         models=[m[0] for m in models if m[0]],
                         vendors=[v[0] for v in vendors if v[0]],
                         sort_by=sort_by,
                         sort_order=sort_order)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """软件上传页面"""
    # 获取所有唯一的软件名称
    software_names = db.session.query(Software.name).distinct().order_by(Software.name).all()
    software_list = [name[0] for name in software_names if name[0]]
    
    # 获取所有唯一的类型和机型
    types = db.session.query(Software.type).distinct().order_by(Software.type).all()
    type_list = [t[0] for t in types if t[0]]
    
    models = db.session.query(Software.model).distinct().order_by(Software.model).all()
    model_list = [m[0] for m in models if m[0]]
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('未选择文件')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('未选择文件')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            try:
                # 验证必填字段
                required_fields = ['type', 'name', 'partnumber']
                for field in required_fields:
                    if not request.form.get(field):
                        flash(f'请填写{field}字段')
                        return redirect(request.url)
                
                # 检查文件名是否重复
                original_filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], original_filename)
                
                # 检查文件是否已存在
                existing_file = File.query.filter_by(original_filename=original_filename).first()
                if existing_file:
                    # 获取已存在文件的软件信息
                    existing_software = Software.query.get(existing_file.software_id)
                    flash(f'文件名 "{original_filename}" 已存在！\n'
                          f'相关信息：\n'
                          f'软件类型：{existing_software.type}\n'
                          f'软件名称：{existing_software.name}\n'
                          f'软件件号：{existing_software.partnumber}\n'
                          f'上传时间：{existing_file.upload_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
                          f'请更改文件名后重新上传。')
                    return redirect(request.url)
                
                # 保存上传的文件，使用原始文件名
                file.save(file_path)
                
                # 获取表单数据
                software = Software(
                    type=request.form['type'],
                    model=request.form.get('model', ''),
                    vendor=request.form.get('vendor', ''),
                    name=request.form['name'],
                    partnumber=request.form['partnumber'],
                    mediapn=request.form.get('mediapn', ''),
                    description=request.form.get('description', ''),
                    creator=request.form.get('creator', '系统'),
                    status_release=True,  # 上传时自动设置为已发布
                    status_allow=False,
                    status_install=False,
                    status_receive=False,
                    release_date=datetime.now()
                )
                
                # 生成COC PDF文件名（这个可以保留时间戳，因为它是内部文档）
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                pdf_filename = f"{software.type}_{software.model}_{software.vendor}_{software.name}_{software.partnumber}_COC_{timestamp}.pdf"
                pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], pdf_filename)
                
                # 生成COC PDF
                generate_coc_pdf(software, pdf_path)
                
                # 保存文件记录
                file_record = File(
                    file_path=file_path,
                    original_filename=original_filename,
                    coc_path=pdf_path,
                    software=software
                )
                
                db.session.add(software)
                db.session.add(file_record)
                db.session.commit()
                
                # 记录上传操作日志
                log_description = (
                    f"上传软件：\n"
                    f"类型：{software.type}\n"
                    f"机型：{software.model}\n"
                    f"厂家：{software.vendor}\n"
                    f"名称：{software.name}\n"
                    f"件号：{software.partnumber}\n"
                    f"文件：{original_filename}"
                )
                log_operation("上传软件", log_description, operator=request.form.get('creator', '系统'))
                
                flash('软件上传成功')
                return redirect(url_for('index'))
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'上传失败: {str(e)}')
                flash(f'上传失败: {str(e)}')
                return redirect(request.url)
                
        else:
            flash('不支持的文件类型')
            return redirect(request.url)
            
    return render_template('upload.html',
                         software_list=software_list,
                         type_list=type_list,
                         model_list=model_list)

@app.route('/api/software_options')
def software_options():
    """获取软件选项API"""
    type_filter = request.args.get('type')
    model_filter = request.args.get('model')
    
    # 构建查询
    models = []
    names = []
    
    if type_filter:
        # 获取指定类型的机型
        models_query = db.session.query(Software.model)\
            .filter(Software.type == type_filter)\
            .filter(Software.model.isnot(None))\
            .filter(Software.model != '')\
            .distinct()\
            .order_by(Software.model)
        models = [m[0] for m in models_query.all()]
        
        # 构建软件名称查询
        names_query = db.session.query(Software.name)\
            .filter(Software.type == type_filter)
        
        # 如果指定了机型，进一步过滤
        if model_filter:
            names_query = names_query.filter(Software.model == model_filter)
        
        # 获取软件名称
        names_query = names_query\
            .filter(Software.name.isnot(None))\
            .filter(Software.name != '')\
            .distinct()\
            .order_by(Software.name)
        names = [n[0] for n in names_query.all()]
    
    return jsonify({
        'models': models,
        'names': names
    })

@app.route('/download_coc/<int:software_id>')
def download_coc(software_id):
    """下载软件COC文档"""
    file_record = File.query.filter_by(software_id=software_id).first()
    if file_record and file_record.coc_path and os.path.exists(file_record.coc_path):
        return send_file(
            file_record.coc_path,
            as_attachment=True,
            download_name=os.path.basename(file_record.coc_path)
        )
    flash('COC文档不存在')
    return redirect(url_for('index'))

@app.route('/download_software/<int:software_id>')
def download_software(software_id):
    """下载软件文件"""
    file_record = File.query.filter_by(software_id=software_id).first()
    if file_record and file_record.file_path and os.path.exists(file_record.file_path):
        return send_file(
            file_record.file_path,
            as_attachment=True,
            download_name=os.path.basename(file_record.file_path)
        )
    flash('软件文件不存在')
    return redirect(url_for('index'))

@app.route('/assistant')
def assistant():
    """软件制作助手页面"""
    return render_template('assistant.html')

@app.route('/api/tree_data')
def get_tree_data():
    """获取文档树数据"""
    # 定义静态目录结构
    result = [
        {
            'id': 'type_ORT',
            'text': 'ORT',
            'children': [
                {
                    'id': 'model_ORT_B737NG',
                    'text': 'B737NG',
                    'type': 'model'
                },
                {
                    'id': 'model_ORT_B737-8',
                    'text': 'B737-8',
                    'type': 'model'
                },
                {
                    'id': 'model_ORT_B747-400',
                    'text': 'B747-400',
                    'type': 'model'
                },
                {
                    'id': 'model_ORT_B747-8',
                    'text': 'B747-8',
                    'type': 'model'
                },
                {
                    'id': 'model_ORT_B777-300ER',
                    'text': 'B777-300ER',
                    'type': 'model'
                },
                {
                    'id': 'model_ORT_A319',
                    'text': 'A319',
                    'type': 'model'
                }
            ]
        },
        {
            'id': 'type_ACMS',
            'text': 'ACMS',
            'children': [
                {
                    'id': 'doc_ACMS_通用',
                    'text': '系统概述',
                    'type': 'doc'
                },
                {
                    'id': 'doc_ACMS_AGSiv',
                    'text': 'AGSiv手册',
                    'type': 'doc'
                }
            ]
        }
    ]
    
    return jsonify(result)

@app.route('/api/document')
def get_document():
    """获取文档内容"""
    type_name = request.args.get('type')
    model = request.args.get('model')
    
    if not type_name:
        return jsonify({'content': ''})
    
    # 根据类型选择对应的文档文件
    docs_path_map = {
        'ORT': os.path.join(current_app.static_folder, 'docs', 'ort_docs.md'),
        'ACMS': os.path.join(current_app.static_folder, 'docs', 'acms_docs.md')
    }
    
    docs_path = docs_path_map.get(type_name)
    if not docs_path:
        return jsonify({'content': '未找到相关文档'})
    
    # 初始化markdown处理器
    processor = MarkdownProcessor(docs_path)
    
    # 获取文档内容
    content = processor.get_section_content(type_name, model)
    
    return jsonify({'content': content})

@app.route('/assistant/manage')
def manage_documents():
    """文档管理页面"""
    docs = ProcessDocument.query.order_by(
        ProcessDocument.type,
        ProcessDocument.doc_type
    ).all()
    return render_template('manage_documents.html', docs=docs)

@app.route('/assistant/edit/<int:doc_id>', methods=['GET', 'POST'])
def edit_document(doc_id):
    """编辑文档"""
    doc = ProcessDocument.query.get_or_404(doc_id)
    
    if request.method == 'POST':
        doc.title = request.form['title']
        doc.content = request.form['content']
        doc.update_time = datetime.now()
        db.session.commit()
        flash('文档更新成功')
        return redirect(url_for('manage_documents'))
        
    return render_template('edit_document.html', doc=doc)

@app.route('/assistant/add', methods=['GET', 'POST'])
def add_document():
    """添加新文档"""
    if request.method == 'POST':
        doc = ProcessDocument(
            type=request.form['type'],
            doc_type=request.form['doc_type'],
            title=request.form['title'],
            content=request.form['content']
        )
        db.session.add(doc)
        db.session.commit()
        flash('文档添加成功')
        return redirect(url_for('manage_documents'))
        
    return render_template('add_document.html')

@app.route('/delete_software/<int:software_id>', methods=['POST'])
def delete_software(software_id):
    """删除软件记录"""
    password = request.form.get('password')
    if password != ADMIN_PASSWORD:
        flash('密码错误，删除失败')
        return redirect(url_for('index'))
    
    try:
        # 获取软件记录
        software = Software.query.get_or_404(software_id)
        file_record = File.query.filter_by(software_id=software_id).first()
        
        if file_record:
            # 删除软件文件
            if os.path.exists(file_record.file_path):
                os.remove(file_record.file_path)
            
            # 删除COC文件
            if file_record.coc_path and os.path.exists(file_record.coc_path):
                os.remove(file_record.coc_path)
            
            # 记录日志
            log_description = (
                f"删除软件记录：\n"
                f"类型：{software.type}\n"
                f"机型：{software.model}\n"
                f"厂家：{software.vendor}\n"
                f"名称：{software.name}\n"
                f"件号：{software.partnumber}\n"
                f"文件：{file_record.original_filename}"
            )
            
            # 删除数据库记录
            db.session.delete(file_record)
        
        db.session.delete(software)
        db.session.commit()
        
        # 记录操作日志
        log_operation("删除软件", log_description, operator="管理员")
        
        flash('软件记录删除成功')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'删除失败: {str(e)}')
        flash(f'删除失败: {str(e)}')
    
    return redirect(url_for('index'))

@app.after_request
def add_security_headers(response):
    """添加安全性和缓存控制头"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # 根据文件扩展名设置正确的Content-Type
    if request.path.endswith('.css'):
        response.headers['Content-Type'] = 'text/css; charset=utf-8'
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    elif request.path.endswith('.html'):
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    
    return response

@app.route('/docs/ACMS/agsiv manual/<path:filename>')
def serve_agsiv_manual(filename):
    """提供AGSiv手册HTML文件"""
    docs_dir = os.path.join(current_app.root_path, '..', 'docs', 'ACMS', 'agsiv manual')
    try:
        # 处理文件名大小写不敏感
        actual_filename = None
        for file in os.listdir(docs_dir):
            if file.lower() == filename.lower():
                actual_filename = file
                break
        
        if actual_filename:
            file_path = os.path.join(docs_dir, actual_filename)
            try:
                # 使用html_processor处理文件
                content, encoding = process_html_file(file_path)
                
                # 返回处理后的内容
                response = current_app.response_class(
                    content,
                    mimetype=f'text/html; charset=utf-8'
                )
                return response
            except Exception as e:
                app.logger.error(f'处理HTML文件失败: {str(e)}')
                return f'处理HTML文件失败: {str(e)}', 500
        else:
            app.logger.error(f'文件不存在: {filename}')
            return f'文件不存在: {filename}', 404
    except Exception as e:
        app.logger.error(f'访问AGSiv手册文件失败: {str(e)}')
        return f'文件访问错误: {str(e)}', 500

@app.route('/docs/ACMS/agsiv manual/<path:subpath>/<path:filename>')
def serve_agsiv_manual_resources(subpath, filename):
    """提供AGSiv手册相关资源文件"""
    docs_dir = os.path.join(current_app.root_path, '..', 'docs', 'ACMS', 'agsiv manual', subpath)
    try:
        response = send_from_directory(docs_dir, filename)
        return response
    except Exception as e:
        app.logger.error(f'访问资源文件失败: {str(e)}')
        return f'资源文件不存在或无法访问', 404 