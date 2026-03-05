
import re
import html
from html.parser import HTMLParser
from typing import Set, Dict, List


class XSSFilter:
    """XSS过滤器 - 用于清理和过滤潜在的XSS攻击代码"""
    
    # 允许的HTML标签白名单
    ALLOWED_TAGS: Set[str] = {
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code', 'div',
        'em', 'i', 'li', 'ol', 'p', 'pre', 'span', 'strong', 'ul',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'table', 'thead',
        'tbody', 'tr', 'th', 'td'
    }
    
    # 允许的属性白名单
    ALLOWED_ATTRS: Dict[str, Set[str]] = {
        'a': {'href', 'title', 'target'},
        'img': {'src', 'alt', 'title', 'width', 'height'},
        'div': {'class', 'id'},
        'span': {'class', 'id'},
        'p': {'class', 'id'},
        '*': {'class', 'id'}
    }
    
    # 危险的协议
    DANGEROUS_PROTOCOLS = {
        'javascript:', 'data:', 'vbscript:', 'file:', 'about:'
    }
    
    # XSS攻击模式
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>.*?</iframe>',
        r'<object[^>]*>.*?</object>',
        r'<embed[^>]*>',
        r'<applet[^>]*>.*?</applet>',
        r'<meta[^>]*>',
        r'<link[^>]*>',
        r'<style[^>]*>.*?</style>',
        r'expression\s*\(',
        r'import\s+',
        r'@import',
        r'<base[^>]*>'
    ]
    
    def __init__(self, allowed_tags: Set[str] = None, allowed_attrs: Dict[str, Set[str]] = None):
        """初始化XSS过滤器"""
        self.allowed_tags = allowed_tags or self.ALLOWED_TAGS
        self.allowed_attrs = allowed_attrs or self.ALLOWED_ATTRS
        self.xss_pattern = re.compile('|'.join(self.XSS_PATTERNS), re.IGNORECASE | re.DOTALL)
    
    def filter(self, text: str) -> str:
        """主过滤方法"""
        if not text:
            return ''
        
        # 1. 基础清理
        text = self._normalize_input(text)
        
        # 2. 移除明显的XSS模式
        text = self._remove_xss_patterns(text)
        
        # 3. 解析和清理HTML
        text = self._parse_and_clean_html(text)
        
        return text
    
    def _normalize_input(self, text: str) -> str:
        """标准化输入"""
        # 移除null字节
        text = text.replace('\x00', '')
        
        # 解码HTML实体多次以防止双重编码绕过
        for _ in range(3):
            decoded = html.unescape(text)
            if decoded == text:
                break
            text = decoded
        
        # 标准化空白字符
        text = re.sub(r'[\r\n\t]+', ' ', text)
        
        return text
    
    def _remove_xss_patterns(self, text: str) -> str:
        """移除已知的XSS攻击模式"""
        text = self.xss_pattern.sub('', text)
        
        # 移除事件处理器
        text = re.sub(r'\bon\w+\s*=\s*["\']?[^"\'>\s]+["\']?', '', text, flags=re.IGNORECASE)
        
        return text
    
    def _parse_and_clean_html(self, text: str) -> str:
        """解析并清理HTML"""
        parser = SafeHTMLParser(self.allowed_tags, self.allowed_attrs)
        try:
            parser.feed(text)
            return parser.get_output()
        except Exception:
            # 如果解析失败，返回转义的文本
            return html.escape(text)
    
    def escape(self, text: str) -> str:
        """完全转义HTML - 用于不允许任何HTML的场景"""
        if not text:
            return ''
        return html.escape(text, quote=True)
    
    def filter_url(self, url: str) -> str:
        """过滤URL中的XSS"""
        if not url:
            return ''
        
        url = url.strip()
        url_lower = url.lower()
        
        # 检查危险协议
        for protocol in self.DANGEROUS_PROTOCOLS:
            if url_lower.startswith(protocol):
                return ''
        
        # 移除危险字符
        url = re.sub(r'[<>"\']', '', url)
        
        return url


class SafeHTMLParser(HTMLParser):
    """安全的HTML解析器"""
    
    def __init__(self, allowed_tags: Set[str], allowed_attrs: Dict[str, Set[str]]):
        super().__init__()
        self.allowed_tags = allowed_tags
        self.allowed_attrs = allowed_attrs
        self.output: List[str] = []
        self.current_tag = None
    
    def handle_starttag(self, tag: str, attrs: List[tuple]):
        """处理开始标签"""
        if tag.lower() in self.allowed_tags:
            self.current_tag = tag.lower()
            clean_attrs = self._filter_attributes(tag.lower(), attrs)
            
            if clean_attrs:
                attrs_str = ' '.join([f'{k}="{html.escape(v)}"' for k, v in clean_attrs])
                self.output.append(f'<{tag} {attrs_str}>')
            else:
                self.output.append(f'<{tag}>')
    
    def handle_endtag(self, tag: str):
        """处理结束标签"""
        if tag.lower() in self.allowed_tags:
            self.output.append(f'</{tag}>')
            self.current_tag = None
    
    def handle_data(self, data: str):
        """处理文本数据"""
        self.output.append(html.escape(data))
    
    def handle_startendtag(self, tag: str, attrs: List[tuple]):
        """处理自闭合标签"""
        if tag.lower() in self.allowed_tags:
            clean_attrs = self._filter_attributes(tag.lower(), attrs)
            
            if clean_attrs:
                attrs_str = ' '.join([f'{k}="{html.escape(v)}"' for k, v in clean_attrs])
                self.output.append(f'<{tag} {attrs_str} />')
            else:
                self.output.append(f'<{tag} />')
    
    def _filter_attributes(self, tag: str, attrs: List[tuple]) -> List[tuple]:
        """过滤属性"""
        clean_attrs = []
        
        # 获取该标签允许的属性
        tag_allowed = self.allowed_attrs.get(tag, set())
        global_allowed = self.allowed_attrs.get('*', set())
        allowed = tag_allowed | global_allowed
        
        for attr_name, attr_value in attrs:
            attr_name_lower = attr_name.lower()
            
            # 检查属性是否在白名单中
            if attr_name_lower not in allowed:
                continue
            
            # 特殊处理href和src属性
            if attr_name_lower in ('href', 'src'):
                attr_value = self._sanitize_url(attr_value)
                if not attr_value:
                    continue
            
            # 移除事件处理器
            if attr_name_lower.startswith('on'):
                continue
            
            clean_attrs.append((attr_name, attr_value))
        
        return clean_attrs
    
    def _sanitize_url(self, url: str) -> str:
        """清理URL"""
        if not url:
            return ''
        
        url = url.strip()
        url_lower = url.lower()
        
        # 检查危险协议
        dangerous_protocols = ['javascript:', 'data:', 'vbscript:', 'file:', 'about:']
        for protocol in dangerous_protocols:
            if url_lower.startswith(protocol):
                return ''
        
        return url
    
    def get_output(self) -> str:
        """获取清理后的输出"""
        return ''.join(self.output)


# 便捷函数
def filter_xss(text: str, allowed_tags: Set[str] = None, allowed_attrs: Dict[str, Set[str]] = None) -> str:
    """过滤XSS攻击代码"""
    xss_filter = XSSFilter(allowed_tags, allowed_attrs)
    return xss_filter.filter(text)


def escape_html(text: str) -> str:
    """完全转义HTML"""
    xss_filter = XSSFilter()
    return xss_filter.escape(text)


def filter_url(url: str) -> str:
    """过滤URL中的XSS"""
    xss_filter = XSSFilter()
    return xss_filter.filter_url(url)
