from html.parser import HTMLParser
from html import escape, unescape
import re


class HTMLCleaner:
    """HTML清理类，用于清理和净化HTML内容"""
    
    # 允许的标签
    ALLOWED_TAGS = {
        'a', 'abbr', 'b', 'blockquote', 'br', 'code', 'div', 'em', 
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'img', 'li', 'ol', 
        'p', 'pre', 'span', 'strong', 'ul', 'table', 'tbody', 'td', 
        'th', 'thead', 'tr'
    }
    
    # 允许的属性
    ALLOWED_ATTRS = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'div': ['class', 'id'],
        'span': ['class', 'id'],
        'p': ['class', 'id'],
        'table': ['class', 'id'],
        'td': ['colspan', 'rowspan'],
        'th': ['colspan', 'rowspan']
    }
    
    # 允许的协议
    ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']
    
    def __init__(self, allowed_tags=None, allowed_attrs=None):
        self.allowed_tags = allowed_tags or self.ALLOWED_TAGS
        self.allowed_attrs = allowed_attrs or self.ALLOWED_ATTRS
        
    def clean(self, html):
        """清理HTML内容"""
        if not html:
            return ''
        
        parser = SafeHTMLParser(self.allowed_tags, self.allowed_attrs)
        parser.feed(html)
        return parser.get_clean_html()
    
    def strip_tags(self, html):
        """移除所有HTML标签，只保留文本"""
        if not html:
            return ''
        
        parser = StripTagsParser()
        parser.feed(html)
        return parser.get_text()
    
    def sanitize_url(self, url):
        """净化URL，防止XSS"""
        if not url:
            return ''
        
        url = url.strip()
        
        # 检查危险协议
        if re.match(r'^(javascript|data|vbscript):', url, re.I):
            return ''
        
        # 检查允许的协议
        if '://' in url:
            protocol = url.split('://')[0].lower()
            if protocol not in self.ALLOWED_PROTOCOLS:
                return ''
        
        return url


class SafeHTMLParser(HTMLParser):
    """安全的HTML解析器"""
    
    def __init__(self, allowed_tags, allowed_attrs):
        super().__init__()
        self.allowed_tags = allowed_tags
        self.allowed_attrs = allowed_attrs
        self.result = []
        self.tag_stack = []
        
    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.allowed_tags:
            # 过滤属性
            safe_attrs = []
            allowed = self.allowed_attrs.get(tag.lower(), [])
            
            for attr, value in attrs:
                if attr.lower() in allowed:
                    # 净化属性值
                    if attr.lower() in ['href', 'src']:
                        value = self._sanitize_url(value)
                        if not value:
                            continue
                    
                    safe_attrs.append(f'{attr}="{escape(value)}"')
            
            attrs_str = ' ' + ' '.join(safe_attrs) if safe_attrs else ''
            self.result.append(f'<{tag}{attrs_str}>')
            self.tag_stack.append(tag)
    
    def handle_endtag(self, tag):
        if tag.lower() in self.allowed_tags and self.tag_stack and self.tag_stack[-1] == tag:
            self.result.append(f'</{tag}>')
            self.tag_stack.pop()
    
    def handle_data(self, data):
        self.result.append(escape(data))
    
    def handle_startendtag(self, tag, attrs):
        if tag.lower() in self.allowed_tags:
            safe_attrs = []
            allowed = self.allowed_attrs.get(tag.lower(), [])
            
            for attr, value in attrs:
                if attr.lower() in allowed:
                    if attr.lower() in ['href', 'src']:
                        value = self._sanitize_url(value)
                        if not value:
                            continue
                    safe_attrs.append(f'{attr}="{escape(value)}"')
            
            attrs_str = ' ' + ' '.join(safe_attrs) if safe_attrs else ''
            self.result.append(f'<{tag}{attrs_str} />')
    
    def _sanitize_url(self, url):
        """净化URL"""
        if not url:
            return ''
        
        url = url.strip()
        
        if re.match(r'^(javascript|data|vbscript):', url, re.I):
            return ''
        
        return url
    
    def get_clean_html(self):
        return ''.join(self.result)


class StripTagsParser(HTMLParser):
    """移除所有标签的解析器"""
    
    def __init__(self):
        super().__init__()
        self.text = []
    
    def handle_data(self, data):
        self.text.append(data)
    
    def get_text(self):
        return ''.join(self.text)


# 使用示例
if __name__ == '__main__':
    cleaner = HTMLCleaner()
    
    # 测试1: 清理危险HTML
    dirty_html = '''
        <div>
            <script>alert('XSS')</script>
            <p>正常文本</p>
            <a href="javascript:alert('XSS')">危险链接</a>
            <a href="https://example.com">安全链接</a>
            <img src="https://example.com/image.jpg" alt="图片" />
        </div>
    '''
    
    clean_html = cleaner.clean(dirty_html)
    print("清理后的HTML:")
    print(clean_html)
    print()
    
    # 测试2: 移除所有标签
    text_only = cleaner.strip_tags(dirty_html)
    print("纯文本:")
    print(text_only)