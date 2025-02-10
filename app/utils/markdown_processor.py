import re
import markdown
from typing import Dict, List, Tuple

class MarkdownProcessor:
    """Markdown文档处理器
    
    用于处理带有特定标记的markdown文档，将其解析为结构化的内容
    """
    
    def __init__(self, markdown_file_path: str):
        """初始化处理器
        
        Args:
            markdown_file_path: markdown文件路径
        """
        self.file_path = markdown_file_path
        self.content = self._read_file()
        
    def _read_file(self) -> str:
        """读取markdown文件内容"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ''
            
    def parse_sections(self) -> List[Dict]:
        """解析文档中的所有段落
        
        Returns:
            包含所有段落信息的列表，每个段落包含type、model和content
        """
        # 定义标记的正则表达式
        section_pattern = r'<!-- BEGIN:TYPE=(.+?)(?:,MODEL=(.+?))? -->\n(.*?)\n<!-- END:TYPE=\1(?:,MODEL=\2)? -->'
        
        # 查找所有匹配的段落
        sections = []
        for match in re.finditer(section_pattern, self.content, re.DOTALL):
            type_name, model, content = match.groups()
            
            # 将markdown内容转换为HTML
            html_content = markdown.markdown(content.strip(), extensions=['extra'])
            
            section = {
                'type': type_name.strip(),
                'content': html_content
            }
            
            # 只有当MODEL存在时才添加
            if model:
                section['model'] = model.strip()
            
            sections.append(section)
            
        return sections
        
    def get_section_content(self, type_name: str, model: str = None) -> str:
        """获取指定段落的内容
        
        Args:
            type_name: 文档类型
            model: 机型（可选）
            
        Returns:
            段落的HTML内容
        """
        sections = self.parse_sections()
        
        # 构建匹配条件
        conditions = lambda s: (
            s['type'] == type_name and
            (not model or s.get('model') == model)
        )
        
        matching_sections = [s for s in sections if conditions(s)]
        
        if not matching_sections:
            return ''
            
        return matching_sections[0]['content'] 