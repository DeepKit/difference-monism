
import re
import html
from typing import Optional


class XSSFilter:
    """XSS过滤器类，提供HTML转义和脚本过滤功能"""
    
    # 危险标签列表
    DANGEROUS_TAGS = [
        'script', 'iframe', 'object', 'embed', 'applet',
        'meta', 'link', 'style', 'base', 'form'
    ]
    
    # 危险属性列表
    DANGEROUS_ATTRS = [
        'onload', 'onerror', 'onclick', 'onmouseover', 'onmouseout',
        'onmousemove', 'onmouseenter', 'onmouseleave', 'onfocus',
        'onblur', 'onchange', 'onsubmit', 'onkeydown', 'onkeyup',
        'onkeypress', 'ondblclick', 'oncontextmenu', 'oninput',
        'onpaste', 'oncopy', 'oncut', 'ondrag', 'ondrop'
    ]
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self):
        """编译正则表达式模式"""
        # 匹配script标签
        self.script_pattern = re.compile(
            r'<script[^>]*>.*?</script>',
            re.IGNORECASE | re.DOTALL
        )
        
        # 匹配危险标签
        tags = '|'.join(self.DANGEROUS_TAGS)
        self.dangerous_tag_pattern = re.compile(
            rf'<({tags})[^>]*>.*?</\1>|<({tags})[^>]*/>',
            re.IGNORECASE | re.DOTALL
        )
        
        # 匹配事件处理器属性
        attrs = '|'.join(self.DANGEROUS_ATTRS)
        self.event_handler_pattern = re.compile(
            rf'\s+({attrs})\s*=\s*["\']?[^"\'>\s]*["\']?',
            re.IGNORECASE
        )
        
        # 匹配javascript:协议
        self.javascript_protocol_pattern = re.compile(
            r'javascript\s*:',
            re.IGNORECASE
        )
        
        # 匹配data:协议
        self.data_protocol_pattern = re.compile(
            r'data\s*:.*?base64',
            re.IGNORECASE
        )
    
    def escape_html(self, text: str) -> str:
        """
        HTML转义
        
        Args:
            text: 需要转义的文本
            
        Returns:
            转义后的文本
        """
        if not text:
            return text
        return html.escape(text, quote=True)
    
    def unescape_html(self, text: str) -> str:
        """
        HTML反转义
        
        Args:
            text: 需要反转义的文本
            
        Returns:
            反转义后的文本
        """
        if not text:
            return text
        return html.unescape(text)
    
    def remove_scripts(self, text: str) -> str:
        """
        移除script标签
        
        Args:
            text: 需要过滤的文本
            
        Returns:
            过滤后的文本
        """
        if not text:
            return text
        return self.script_pattern.sub('', text)
    
    def remove_dangerous_tags(self, text: str) -> str:
        """
        移除危险标签
        
        Args:
            text: 需要过滤的文本
            
        Returns:
            过滤后的文本
        """
        if not text:
            return text
        return self.dangerous_tag_pattern.sub('', text)
    
    def remove_event_handlers(self, text: str) -> str:
        """
        移除事件处理器属性
        
        Args:
            text: 需要过滤的文本
            
        Returns:
            过滤后的文本
        """
        if not text:
            return text
        return self.event_handler_pattern.sub('', text)
    
    def remove_javascript_protocol(self, text: str) -> str:
        """
        移除javascript:协议
        
        Args:
            text: 需要过滤的文本
            
        Returns:
            过滤后的文本
        """
        if not text:
            return text
        return self.javascript_protocol_pattern.sub('', text)
    
    def remove_data_protocol(self, text: str) -> str:
        """
        移除data:协议
        
        Args:
            text: 需要过滤的文本
            
        Returns:
            过滤后的文本
        """
        if not text:
            return text
        return self.data_protocol_pattern.sub('', text)
    
    def filter(self, text: str, escape: bool = False) -> str:
        """
        综合过滤方法
        
        Args:
            text: 需要过滤的文本
            escape: 是否进行HTML转义
            
        Returns:
            过滤后的文本
        """
        if not text:
            return text
        
        # 移除危险内容
        text = self.remove_scripts(text)
        text = self.remove_dangerous_tags(text)
        text = self.remove_event_handlers(text)
        text = self.remove_javascript_protocol(text)
        text = self.remove_data_protocol(text)
        
        # 可选HTML转义
        if escape:
            text = self.escape_html(text)
        
        return text
    
    def sanitize(self, text: str) -> str:
        """
        严格清理模式（HTML转义）
        
        Args:
            text: 需要清理的文本
            
        Returns:
            清理后的文本
        """
        return self.escape_html(text)
    
    def clean(self, text: str) -> str:
        """
        宽松清理模式（仅移除危险内容）
        
        Args:
            text: 需要清理的文本
            
        Returns:
            清理后的文本
        """
        return self.filter(text, escape=False)


# 使用示例
if __name__ == '__main__':
    xss_filter = XSSFilter()
    
    # 测试用例
    test_cases = [
        '<script>alert("XSS")</script>',
        '<img src="x" onerror="alert(1)">',
        '<a href="javascript:alert(1)">Click</a>',
        '<div onclick="alert(1)">Click me</div>',
        '<iframe src="evil.com"></iframe>',
        'Normal text with <b>bold</b>',
        '<img src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">',
    ]
    
    print("=== HTML转义测试 ===")
    for test in test_cases:
        print(f"原始: {test}")
        print(f"转义: {xss_filter.escape_html(test)}\n")
    
    print("\n=== 脚本过滤测试 ===")
    for test in test_cases:
        print(f"原始: {test}")
        print(f"过滤: {xss_filter.filter(test)}\n")
    
    print("\n=== 严格清理测试 ===")
    for test in test_cases:
        print(f"原始: {test}")
        print(f"清理: {xss_filter.sanitize(test)}\n")
