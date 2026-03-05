import re
from collections import Counter
from typing import List

class TextSummarizer:
    def __init__(self, language: str = 'en'):
        self.language = language
        
    def summarize(self, text: str, num_sentences: int = 3) -> str:
        """提取文本摘要"""
        sentences = self._split_sentences(text)
        if len(sentences) <= num_sentences:
            return text
            
        # 计算词频
        words = self._tokenize(text.lower())
        word_freq = Counter(words)
        
        # 移除停用词后的词频
        word_freq = {w: f for w, f in word_freq.items() if len(w) > 2}
        
        # 归一化词频
        max_freq = max(word_freq.values()) if word_freq else 1
        word_freq = {w: f/max_freq for w, f in word_freq.items()}
        
        # 计算句子得分
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words_in_sentence = self._tokenize(sentence.lower())
            score = sum(word_freq.get(w, 0) for w in words_in_sentence)
            sentence_scores[i] = score / len(words_in_sentence) if words_in_sentence else 0
        
        # 选择得分最高的句子
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])  # 保持原顺序
        
        return ' '.join(sentences[i] for i, _ in top_sentences)
    
    def _split_sentences(self, text: str) -> List[str]:
        """分割句子"""
        sentences = re.split(r'[.!?。！？]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _tokenize(self, text: str) -> List[str]:
        """分词"""
        return re.findall(r'\b\w+\b', text)


# 使用示例
if __name__ == '__main__':
    summarizer = TextSummarizer()
    
    text = """
    Artificial intelligence is transforming the world. Machine learning algorithms 
    can now process vast amounts of data. Deep learning has revolutionized computer 
    vision and natural language processing. AI systems are being deployed across 
    various industries. The future of AI looks promising with continued research 
    and development.
    """
    
    summary = summarizer.summarize(text, num_sentences=2)
    print(summary)