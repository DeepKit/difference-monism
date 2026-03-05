import re
from pathlib import Path
from typing import Union


class TextExtractor:
    """文本提取器，支持多种格式"""
    
    def __init__(self):
        self.extractors = {
            '.txt': self._extract_txt,
            '.pdf': self._extract_pdf,
            '.docx': self._extract_docx,
            '.html': self._extract_html,
        }
    
    def extract(self, file_path: Union[str, Path]) -> str:
        """提取文件文本"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        ext = path.suffix.lower()
        extractor = self.extractors.get(ext)
        
        if not extractor:
            raise ValueError(f"不支持的文件格式: {ext}")
        
        return extractor(path)
    
    def _extract_txt(self, path: Path) -> str:
        """提取TXT文本"""
        return path.read_text(encoding='utf-8', errors='ignore')
    
    def _extract_pdf(self, path: Path) -> str:
        """提取PDF文本"""
        try:
            import PyPDF2
            text = []
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        except ImportError:
            raise ImportError("需要安装 PyPDF2: pip install PyPDF2")
    
    def _extract_docx(self, path: Path) -> str:
        """提取DOCX文本"""
        try:
            from docx import Document
            doc = Document(path)
            return '\n'.join([para.text for para in doc.paragraphs])
        except ImportError:
            raise ImportError("需要安装 python-docx: pip install python-docx")
    
    def _extract_html(self, path: Path) -> str:
        """提取HTML文本"""
        try:
            from bs4 import BeautifulSoup
            html = path.read_text(encoding='utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text(separator='\n', strip=True)
        except ImportError:
            raise ImportError("需要安装 beautifulsoup4: pip install beautifulsoup4")
    
    def clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除首尾空白
        text = text.strip()
        return text


# 使用示例
if __name__ == '__main__':
    extractor = TextExtractor()
    
    # 提取文本
    text = extractor.extract('example.txt')
    
    # 清理文本
    clean = extractor.clean_text(text)
    print(clean)