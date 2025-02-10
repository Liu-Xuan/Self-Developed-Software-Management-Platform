import os
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

class PDFTemplate:
    """PDF模板处理类
    
    用于加载PDF模板并根据模板生成PDF文件
    支持自定义模板和默认模板
    """
    
    def __init__(self):
        """初始化PDF模板处理类"""
        self.template = None
        self.font_name = self._get_font()
        
    def _get_font(self):
        """获取可用的中文字体
        
        按优先级尝试不同的中文字体，确保至少有一个可用字体
        """
        # 尝试使用系统字体
        system_fonts = {
            # Windows字体路径
            'SimHei': 'C:\\Windows\\Fonts\\simhei.ttf',
            'SimSun': 'C:\\Windows\\Fonts\\simsun.ttc',
            'Microsoft YaHei': 'C:\\Windows\\Fonts\\msyh.ttc',
            # macOS字体路径
            'STHeiti Light': '/System/Library/Fonts/STHeiti Light.ttc',
            'STSong': '/System/Library/Fonts/STSongti-SC-Regular.ttc',
            'PingFang': '/System/Library/Fonts/PingFang.ttc',
            # Linux字体路径
            'WenQuanYi': '/usr/share/fonts/wenquanyi/wqy-zenhei.ttc'
        }
        
        # 尝试注册系统字体
        for font_name, font_path in system_fonts.items():
            try:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    return font_name
            except:
                continue
                
        # 如果系统字体都不可用，使用内置的中文字体
        try:
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            return 'STSong-Light'
        except:
            # 如果都失败了，使用基本字体
            return 'Helvetica'
            
    def load_template(self, template_path=None):
        """加载PDF模板
        
        Args:
            template_path: 模板文件路径，如果为None则使用默认模板
        """
        if template_path is None:
            # 使用默认模板
            default_template_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'templates',
                'default_coc_template.json'
            )
            template_path = default_template_path
            
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                self.template = json.load(f)
        except Exception as e:
            raise Exception(f'加载模板文件失败: {str(e)}')
            
    def generate(self, data, output_path):
        """根据模板生成PDF文件
        
        Args:
            data: 包含所有字段数据的字典
            output_path: 输出PDF文件的路径
        """
        if self.template is None:
            self.load_template()
            
        # 创建PDF文档
        c = canvas.Canvas(output_path)
        c.setFont(self.font_name, self.template['title']['font_size'])
        
        # 绘制标题
        title_config = self.template['title']
        c.drawString(
            title_config['position'][0],
            title_config['position'][1],
            title_config['text']
        )
        
        # 绘制内容
        content_config = self.template['content']
        current_y = content_config['start_position'][1]
        c.setFont(self.font_name, content_config['font_size'])
        
        # 遍历所有部分
        for section_name, section in content_config['sections'].items():
            # 绘制部分标题
            c.setFont(self.font_name, content_config['font_size'] + 2)
            c.drawString(
                content_config['left_margin'],
                current_y,
                section['title']
            )
            current_y -= content_config['line_spacing']
            
            # 绘制字段
            c.setFont(self.font_name, content_config['font_size'])
            for field in section['fields']:
                label = field['label']
                value = data.get(field['field'], '')
                text = f"{label}: {value}"
                c.drawString(
                    content_config['left_margin'],
                    current_y,
                    text
                )
                current_y -= content_config['line_spacing']
            
            # 部分之间添加额外间距
            current_y -= content_config['line_spacing']
            
        # 绘制页脚
        footer_config = self.template['footer']
        c.setFont(self.font_name, footer_config['font_size'])
        footer_text = footer_config['text'].format(
            generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        c.drawString(
            footer_config['position'][0],
            footer_config['position'][1],
            footer_text
        )
        
        # 保存PDF
        c.save() 