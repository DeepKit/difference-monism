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
        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 去除URL
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        # 去除邮箱
        text = re.sub(r'\S+@\S+', '', text)
        # 统一空白字符
        text = re.sub(r'\s+', ' ', text)
        # 去除首尾空格
        return text.strip()
    
    def normalize_text(self, text: str) -> str:
        """标准化文本：统一标点、大小写等"""
        # 中文标点转英文
        punctuation_map = {
            '，': ',', '。': '.', '！': '!', '？': '?',
            '；': ';', '：': ':', '（': '(', '）': ')',
            '【': '[', '】': ']', '《': '<', '》': '>',
            '"': '"', '"': '"', ''': "'", ''': "'"
        }
        for cn, en in punctuation_map.items():
            text = text.replace(cn, en)
        return text
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[tuple]:
        """提取关键词（基于词频）"""
        # 简单分词（按空格和标点）
        words = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', text)
        # 过滤停用词和短词
        words = [w for w in words if len(w) > 1 and w not in self.stop_words]
        # 统计词频
        word_freq = Counter(words)
        return word_freq.most_common(top_n)
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """生成摘要（提取前N个字符）"""
        cleaned = self.clean_text(text)
        if len(cleaned) <= max_length:
            return cleaned
        return cleaned[:max_length] + '...'
    
    def add_metadata(self, content: str, title: str = '', author: str = '') -> Dict:
        """添加元数据"""
        return {
            'title': title,
            'author': author,
            'content': content,
            'word_count': len(re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', content)),
            'char_count': len(content),
            'created_at': datetime.now().isoformat(),
            'summary': self.generate_summary(content, 100),
            'keywords': self.extract_keywords(content, 5)
        }
    
    def format_paragraphs(self, text: str, indent: int = 2) -> str:
        """格式化段落：添加缩进"""
        paragraphs = text.split('\n')
        indent_str = ' ' * indent
        formatted = [indent_str + p.strip() for p in paragraphs if p.strip()]
        return '\n\n'.join(formatted)
    
    def remove_duplicates(self, text: str) -> str:
        """去除重复句子"""
        sentences = re.split(r'[。.!！?？\n]', text)
        seen = set()
        unique_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence not in seen:
                seen.add(sentence)
                unique_sentences.append(sentence)
        return '。'.join(unique_sentences) + '。'
    
    def enhance(self, text: str, 
                clean: bool = True,
                normalize: bool = True,
                remove_dup: bool = False,
                add_meta: bool = False,
                title: str = '',
                author: str = '') -> Dict:
        """综合增强处理"""
        result = {'original': text}
        
        enhanced_text = text
        if clean:
            enhanced_text = self.clean_text(enhanced_text)
        if normalize:
            enhanced_text = self.normalize_text(enhanced_text)
        if remove_dup:
            enhanced_text = self.remove_duplicates(enhanced_text)
        
        result['enhanced'] = enhanced_text
        
        if add_meta:
            result['metadata'] = self.add_metadata(enhanced_text, title, author)
        
        return result


# 使用示例
if __name__ == '__main__':
    enhancer = ContentEnhancer()
    
    sample_text = """
    这是一个测试文本。这是一个测试文本。
    包含了一些重复的内容，还有   多余的空格。
    网址：https://example.com 和邮箱：test@example.com
    """
    
    # 基础清理
    cleaned = enhancer.clean_text(sample_text)
    print("清理后:", cleaned)
    
    # 提取关键词
    keywords = enhancer.extract_keywords(sample_text)
    print("关键词:", keywords)
    
    # 综合增强
    result = enhancer.enhance(
        sample_text,
        clean=True,
        normalize=True,
        remove_dup=True,
        add_meta=True,
        title="测试文档",
        author="Kiro"
    )
    print("\n增强结果:", result)