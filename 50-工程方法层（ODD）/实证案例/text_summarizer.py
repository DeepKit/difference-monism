import re
from collections import Counter
from typing import List, Optional
import math


class TextSummarizer:
    """文本摘要生成器"""
    
    def __init__(self, language: str = 'zh'):
        """
        初始化摘要器
        
        Args:
            language: 语言类型，'zh'为中文，'en'为英文
        """
        self.language = language
        self.stopwords = self._load_stopwords()
    
    def _load_stopwords(self) -> set:
        """加载停用词"""
        if self.language == 'zh':
            # 中文常见停用词
            return {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', 
                   '都', '一个', '上', '也', '很', '到', '说', '要', '去',
                   '你', '会', '着', '没有', '看', '好', '自己', '这'}
        else:
            # 英文常见停用词
            return {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                   'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
                   'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do',
                   'does', 'did', 'will', 'would', 'could', 'should', 'may',
                   'might', 'must', 'can', 'this', 'that', 'these', 'those'}
    
    def _split_sentences(self, text: str) -> List[str]:
        """分割句子"""
        if self.language == 'zh':
            # 中文句子分割
            sentences = re.split(r'[。！？；\n]+', text)
        else:
            # 英文句子分割
            sentences = re.split(r'[.!?\n]+', text)
        
        return [s.strip() for s in sentences if s.strip()]
    
    def _tokenize(self, text: str) -> List[str]:
        """分词"""
        if self.language == 'zh':
            # 简单的中文分词（按字符）
            words = [char for char in text if char.strip() and char not in '，。！？；：、']
        else:
            # 英文分词
            words = re.findall(r'\b\w+\b', text.lower())
        
        return [w for w in words if w not in self.stopwords]
    
    def _calculate_word_frequencies(self, sentences: List[str]) -> dict:
        """计算词频"""
        all_words = []
        for sentence in sentences:
            all_words.extend(self._tokenize(sentence))
        
        word_freq = Counter(all_words)
        
        # 归一化
        max_freq = max(word_freq.values()) if word_freq else 1
        for word in word_freq:
            word_freq[word] = word_freq[word] / max_freq
        
        return word_freq
    
    def _score_sentences(self, sentences: List[str], word_freq: dict) -> dict:
        """计算句子得分"""
        sentence_scores = {}
        
        for i, sentence in enumerate(sentences):
            words = self._tokenize(sentence)
            if not words:
                sentence_scores[i] = 0
                continue
            
            # 基于词频的得分
            score = sum(word_freq.get(word, 0) for word in words)
            
            # 句子长度惩罚（避免过长或过短的句子）
            length_penalty = 1.0
            if len(words) < 5:
                length_penalty = 0.5
            elif len(words) > 30:
                length_penalty = 0.8
            
            # 位置加权（开头和结尾的句子更重要）
            position_weight = 1.0
            if i < len(sentences) * 0.2:  # 前20%
                position_weight = 1.2
            elif i > len(sentences) * 0.8:  # 后20%
                position_weight = 1.1
            
            sentence_scores[i] = score * length_penalty * position_weight / len(words)
        
        return sentence_scores
    
    def summarize(self, text: str, ratio: float = 0.3, max_sentences: Optional[int] = None) -> str:
        """
        生成摘要
        
        Args:
            text: 原始文本
            ratio: 摘要比例（0-1之间）
            max_sentences: 最大句子数，如果指定则忽略ratio
        
        Returns:
            摘要文本
        """
        if not text.strip():
            return ""
        
        # 分割句子
        sentences = self._split_sentences(text)
        
        if len(sentences) <= 1:
            return text
        
        # 计算词频
        word_freq = self._calculate_word_frequencies(sentences)
        
        # 计算句子得分
        sentence_scores = self._score_sentences(sentences, word_freq)
        
        # 确定摘要句子数量
        if max_sentences:
            num_sentences = min(max_sentences, len(sentences))
        else:
            num_sentences = max(1, int(len(sentences) * ratio))
        
        # 选择得分最高的句子
        top_sentences = sorted(sentence_scores.items(), 
                              key=lambda x: x[1], 
                              reverse=True)[:num_sentences]
        
        # 按原文顺序排列
        top_sentences = sorted(top_sentences, key=lambda x: x[0])
        
        # 生成摘要
        if self.language == 'zh':
            summary = '。'.join(sentences[i] for i, _ in top_sentences) + '。'
        else:
            summary = '. '.join(sentences[i] for i, _ in top_sentences) + '.'
        
        return summary
    
    def summarize_by_length(self, text: str, max_length: int = 200) -> str:
        """
        按字符长度生成摘要
        
        Args:
            text: 原始文本
            max_length: 最大字符长度
        
        Returns:
            摘要文本
        """
        sentences = self._split_sentences(text)
        word_freq = self._calculate_word_frequencies(sentences)
        sentence_scores = self._score_sentences(sentences, word_freq)
        
        # 按得分排序
        sorted_sentences = sorted(sentence_scores.items(), 
                                 key=lambda x: x[1], 
                                 reverse=True)
        
        summary_sentences = []
        current_length = 0
        
        for idx, score in sorted_sentences:
            sentence = sentences[idx]
            if current_length + len(sentence) <= max_length:
                summary_sentences.append((idx, sentence))
                current_length += len(sentence)
            
            if current_length >= max_length * 0.9:
                break
        
        # 按原文顺序排列
        summary_sentences.sort(key=lambda x: x[0])
        
        if self.language == 'zh':
            return '。'.join(s for _, s in summary_sentences) + '。'
        else:
            return '. '.join(s for _, s in summary_sentences) + '.'


# 使用示例
if __name__ == '__main__':
    # 中文示例
    zh_text = """
    人工智能是计算机科学的一个分支。它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。
    可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程进行模拟。
    人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。
    """
    
    summarizer_zh = TextSummarizer(language='zh')
    summary_zh = summarizer_zh.summarize(zh_text, ratio=0.4)
    print("中文摘要：")
    print(summary_zh)
    print()
    
    # 英文示例
    en_text = """
    Artificial intelligence is a branch of computer science. It attempts to understand the essence of intelligence 
    and produce a new intelligent machine that can react in a similar way to human intelligence. Research in this 
    field includes robotics, speech recognition, image recognition, natural language processing and expert systems. 
    Since its birth, artificial intelligence has matured in theory and technology, and its application fields have 
    continued to expand. It can be imagined that future technology products brought by artificial intelligence will 
    be the container of human wisdom. Artificial intelligence can simulate the information process of human 
    consciousness and thinking. Artificial intelligence is not human intelligence, but it can think like humans 
    and may even surpass human intelligence.
    """
    
    summarizer_en = TextSummarizer(language='en')
    summary_en = summarizer_en.summarize(en_text, max_sentences=3)
    print("English Summary:")
    print(summary_en)