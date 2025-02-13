import os
import chardet

def process_html_file(file_path):
    """处理HTML文件的编码和内容
    
    Args:
        file_path: HTML文件路径
        
    Returns:
        tuple: (content, encoding)
    """
    # 首先检测文件编码
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    
    # 读取文件内容
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
    
    # 确保HTML文件包含正确的编码声明
    if content.find('<meta charset=') == -1 and content.find('<meta http-equiv="Content-Type"') == -1:
        if '<head>' in content:
            content = content.replace('<head>', '''<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">''')
        else:
            # 如果没有head标签，添加一个
            content = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
''' + content
    
    return content, encoding 