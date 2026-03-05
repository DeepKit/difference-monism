import re
from typing import List, Tuple


class MarkdownParser:
    """Markdown解析器类"""
    
    def __init__(self):
        self.html = ""
        
    def parse(self, markdown_text: str) -> str:
        """解析Markdown文本为HTML"""
        lines = markdown_text.split('\n')
        self.html = ""
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 代码块
            if line.strip().startswith('