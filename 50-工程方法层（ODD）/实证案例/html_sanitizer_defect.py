from html.parser import HTMLParser
from html import escape, unescape
import re
from typing import Set, Dict, List, Optional


class HTMLCleaner(HTMLParser):
    """HTML清理类，用于清理和净化HTML内容"""
    
    # 默认允许的标签
    DEFAULT_ALLOWED_TAGS = {
        'a', 'abbr', 'b', 'blockquote', 'br', 'code', 'div', 'em', 'i',
        'li', 'ol', 'p', 'pre', 'span', 'strong', 'ul', 'h1', 'h2', 'h3',
        'h4', 'h5', 'h6', 'img', 'table', 'thead', 'tbody', 'tr', 'td', 'th'
    }
    
    # 默认允许的属性
    DEFAULT_ALLOWED_ATTRS = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'div': ['class', 'id'],
        'span': ['class', 'id'],
        'p': ['class', 'id'],
        'table': ['class', 'id'],
        'td': ['colspan', 'rowspan'],
        'th': ['colspan', 'rowspan']
    }
    
    # 危险的协议
    DANGEROUS_PROTOCOLS = ['javascript:', 'data:', 'vbscript:']
    
    def __init__(
        self,
        allowed_tags: Optional[Set[str]] = None,
        allowed_attrs: Optional[Dict[str, List[str]]] = None,
        strip_comments: bool = True,
        strip_scripts: bool = True
    ):
        super().__init__()
        self.allowed_tags = allowed_tags or self.DEFAULT_ALLOWED_TAGS
        self.allowed_attrs = allowed_attrs or self.DEFAULT_ALLOWED_ATTRS
        self.strip_comments = strip_comments
        self.strip_scripts = strip_scripts
        self.result = []
        self.skip_content = False
        
    def handle_starttag(self, tag: str, attrs: List[tuple]):
        if tag in ['script', 'style'] and self.strip_scripts:
            self.skip_content = True
            return
            
        if tag not in self.allowed_tags:
            return
            
        cleaned_attrs = self._clean_attributes(tag, attrs)
        
        if cleaned_attrs:
            attrs_str = ' '.join(f'{k}="{escape(v)}"' for k, v in cleaned_attrs)
            self.result.append(f'<{tag} {attrs_str}>')
        else:
            self.result.append(f'<{tag}>')
    
    def handle_endtag(self, tag: str):
        if tag in ['script', 'style'] and self.strip_scripts:
            self.skip_content = False
            return
            
        if tag in self.allowed_tags:
            self.result.append(f'</{tag}>')
    
    def handle_data(self, data: str):
        if not self.skip_content:
            self.result.append(escape(data))
    
    def handle_comment(self, data: str):
        if not self.strip_comments:
            self.result.append(f'<!--{escape(data)}-->')
    
    def _clean_attributes(self, tag: str, attrs: List[tuple]) -> List[tuple]:
        if tag not in self.allowed_attrs:
            return []
        
        allowed = self.allowed_attrs[tag]
        cleaned = []
        
        for name, value in attrs:
            if name not in allowed:
                continue
                
            # 检查危险协议
            if name in ['href', 'src']:
                if any(value.lower().startswith(proto) for proto in self.DANGEROUS_PROTOCOLS):
                    continue
            
            # 清理属性值
            value = self._sanitize_value(value)
            cleaned.append((name, value))
        
        return cleaned
    
    def _sanitize_value(self, value: str) -> str:
        # 移除潜在的XSS向量
        value = re.sub(r'[\x00-\x1f\x7f]', '', value)
        value = value.replace('\x00', '')
        return value.strip()
    
    def clean(self, html: str) -> str:
        """清理HTML内容"""
        self.result = []
        self.skip_content = False
        self.feed(html)
        return ''.join(self.result)
    
    @classmethod
    def clean_html(
        cls,
        html: str,
        allowed_tags: Optional[Set[str]] = None,
        allowed_attrs: Optional[Dict[str, List[str]]] = None
    ) -> str:
        """便捷的类方法"""
        cleaner = cls(allowed_tags=allowed_tags, allowed_attrs=allowed_attrs)
        return cleaner.clean(html)


# 使用示例
if __name__ == '__main__':
    # 基本使用
    dirty_html = '''
    <div>
        <script>alert('XSS')</script>
        <p onclick="alert('XSS')">Hello <strong>World</strong></p>
        <a href="javascript:alert('XSS')">Bad Link</a>
        <a href="https://example.com">Good Link</a>
        <img src="image.jpg" onerror="alert('XSS')" alt="Image">
    </div>
    '''
    
    cleaner = HTMLCleaner()
    clean_html = cleaner.clean(dirty_html)
    print("清理后的HTML:")
    print(clean_html)
    
    # 自定义配置
    custom_cleaner = HTMLCleaner(
        allowed_tags={'p', 'a', 'strong'},
        allowed_attrs={'a': ['href']}
    )
    print("\n自定义清理:")
    print(custom_cleaner.clean(dirty_html))
    
    # 使用类方法
    print("\n类方法清理:")
    print(HTMLCleaner.clean_html(dirty_html))