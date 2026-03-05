import re
from typing import List, Dict, Optional
from collections import Counter
from datetime import datetime


class ContentEnhancer:
    """内容增强类 - 提供文本清理、分析和增强功能"""
    
    def __init__(self):
        self.stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就', 
                               '不', '人', '都', '一个', '上', '也', '很',
                               '到', '说', '要', '去', '你', '会', '着', '没有',
                               '看', '好', '自己', '这'])
    
    def clean_text(self, text: str) -> str:
        """清理文本：去除多余空格、特殊字符等"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\u4e00-\u9fff,.!?;:，。！？；：]', '', text)
        return text.strip()
    
    def normalize_text(self, text: str) -> str:
        """标准化文本：统一标点、大小写等"""
        text = text.replace('，', ',').replace('。', '.')
        text = text.replace('！', '!').replace('？', '?')
        text = re.sub(r'\.{2,}', '...', text)
        return text
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[tuple]:
        """提取关键词（基于词频）"""
        words = re.findall(r'[\u4e00-\u9fff]+', text)
        words = [w for w in words if len(w) > 1 and w not in self.stop_words]
        word_freq = Counter(words)
        return word_freq.most_common(top_n)
    
    def generate_summary(self, text: str, max_sentences: int = 3) -> str:
        """生成摘要（提取前N个句子）"""
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return '。'.join(sentences[:max_sentences]) + '。'
    
    def count_stats(self, text: str) -> Dict[str, int]:
        """统计文本信息"""
        return {
            'total_chars': len(text),
            'total_words': len(re.findall(r'[\u4e00-\u9fff]+', text)),
            'total_sentences': len(re.split(r'[。！？.!?]', text)),
            'total_paragraphs': len(text.split('\n'))
        }
    
    def add_metadata(self, text: str, title: Optional[str] = None) -> Dict:
        """添加元数据"""
        return {
            'content': text,
            'title': title or '无标题',
            'created_at': datetime.now().isoformat(),
            'stats': self.count_stats(text),
            'keywords': self.extract_keywords(text, 5)
        }
    
    def format_markdown(self, text: str, title: Optional[str] = None) -> str:
        """格式化为Markdown"""
        result = []
        if title:
            result.append(f"# {title}\n")
        
        paragraphs = text.split('\n')
        for para in paragraphs:
            if para.strip():
                result.append(para.strip() + '\n')
        
        return '\n'.join(result)
    
    def enhance(self, text: str, options: Optional[Dict] = None) -> Dict:
        """综合增强：清理、分析、添加元数据"""
        options = options or {}
        
        cleaned = self.clean_text(text)
        normalized = self.normalize_text(cleaned)
        
        result = {
            'original': text,
            'cleaned': cleaned,
            'normalized': normalized,
            'stats': self.count_stats(normalized),
            'keywords': self.extract_keywords(normalized, options.get('top_keywords', 10)),
            'summary': self.generate_summary(normalized, options.get('summary_sentences', 3)),
            'metadata': {
                'processed_at': datetime.now().isoformat(),
                'options': options
            }
        }
        
        return result


# 使用示例
if __name__ == '__main__':
    enhancer = ContentEnhancer()
    
    sample_text = """
    人工智能技术正在快速发展。机器学习和深度学习已经在各个领域得到广泛应用。
    自然语言处理技术让计算机能够理解人类语言。这些技术正在改变我们的生活方式。
    """
    
    # 基本清理
    cleaned = enhancer.clean_text(sample_text)
    print("清理后:", cleaned)
    
    # 提取关键词
    keywords = enhancer.extract_keywords(sample_text)
    print("\n关键词:", keywords)
    
    # 生成摘要
    summary = enhancer.generate_summary(sample_text)
    print("\n摘要:", summary)
    
    # 综合增强
    enhanced = enhancer.enhance(sample_text, {'top_keywords': 5, 'summary_sentences': 2})
    print("\n增强结果:", enhanced)