import re
from typing import List, Tuple


class MarkdownParser:
    def __init__(self):
        self.html = ""
        
    def parse(self, markdown: str) -> str:
        """解析Markdown文本为HTML"""
        lines = markdown.split('\n')
        self.html = ""
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 代码块
            if line.strip().startswith('