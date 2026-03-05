import re
from collections import Counter
from typing import List, Tuple, Dict
import math


class KeywordExtractor:
    """关键词提取器"""
    
    def __init__(self, stopwords: List[str] = None):
        self.stopwords = set(stopwords) if stopwords else set()
        
    def _tokenize(self, text: str) -> List[str]:
        """分词（简单实现，支持中英文）"""
        # 中文按字符分，英文按单词分
        chinese = re.findall(r'[\u4e00-\u9fff]+', text)
        english = re.findall(r'[a-zA-Z]+', text.lower())
        
        tokens = []
        for word in chinese:
            tokens.extend(list(word))
        tokens.extend(english)
        
        return [t for t in tokens if t not in self.stopwords and len(t) > 1]
    
    def extract_by_frequency(self, text: str, top_k: int = 10) -> List[Tuple[str, int]]:
        """基于词频提取关键词"""
        tokens = self._tokenize(text)
        counter = Counter(tokens)
        return counter.most_common(top_k)
    
    def extract_by_tfidf(self, text: str, corpus: List[str] = None, top_k: int = 10) -> List[Tuple[str, float]]:
        """基于TF-IDF提取关键词"""
        tokens = self._tokenize(text)
        tf = Counter(tokens)
        
        # 计算TF
        max_freq = max(tf.values()) if tf else 1
        tf_scores = {word: freq / max_freq for word, freq in tf.items()}
        
        # 计算IDF
        if corpus:
            doc_count = len(corpus)
            df = Counter()
            for doc in corpus:
                doc_tokens = set(self._tokenize(doc))
                df.update(doc_tokens)
            
            idf_scores = {word: math.log(doc_count / (df.get(word, 0) + 1)) 
                         for word in tf_scores}
        else:
            idf_scores = {word: 1.0 for word in tf_scores}
        
        # 计算TF-IDF
        tfidf_scores = {word: tf_scores[word] * idf_scores[word] 
                       for word in tf_scores}
        
        return sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    
    def extract_by_textrank(self, text: str, top_k: int = 10, window: int = 5, 
                           iterations: int = 20, damping: float = 0.85) -> List[Tuple[str, float]]:
        """基于TextRank算法提取关键词"""
        tokens = self._tokenize(text)
        if len(tokens) < 2:
            return []
        
        # 构建共现图
        graph = {}
        for i, word in enumerate(tokens):
            if word not in graph:
                graph[word] = {}
            
            # 窗口内的词建立边
            start = max(0, i - window)
            end = min(len(tokens), i + window + 1)
            
            for j in range(start, end):
                if i != j:
                    neighbor = tokens[j]
                    if neighbor not in graph[word]:
                        graph[word][neighbor] = 0
                    graph[word][neighbor] += 1
        
        # TextRank迭代
        scores = {word: 1.0 for word in graph}
        
        for _ in range(iterations):
            new_scores = {}
            for word in graph:
                rank_sum = 0
                for neighbor, weight in graph[word].items():
                    neighbor_out_sum = sum(graph[neighbor].values())
                    if neighbor_out_sum > 0:
                        rank_sum += (weight / neighbor_out_sum) * scores[neighbor]
                
                new_scores[word] = (1 - damping) + damping * rank_sum
            
            scores = new_scores
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    
    def extract(self, text: str, method: str = 'tfidf', top_k: int = 10, **kwargs) -> List[Tuple[str, float]]:
        """统一接口提取关键词"""
        if method == 'frequency':
            return self.extract_by_frequency(text, top_k)
        elif method == 'tfidf':
            return self.extract_by_tfidf(text, top_k=top_k, **kwargs)
        elif method == 'textrank':
            return self.extract_by_textrank(text, top_k, **kwargs)
        else:
            raise ValueError(f"不支持的方法: {method}")


# 使用示例
if __name__ == "__main__":
    # 中文停用词示例
    stopwords = ['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一个']
    
    extractor = KeywordExtractor(stopwords=stopwords)
    
    text = """
    人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。人工智能从诞生以来，理论和技术日益成熟，
    应用领域也不断扩大，可以设想，未来人工智能带来的科技产品，将会是人类智慧的容器。
    """
    
    print("词频法:")
    print(extractor.extract(text, method='frequency', top_k=5))
    
    print("\nTF-IDF法:")
    print(extractor.extract(text, method='tfidf', top_k=5))
    
    print("\nTextRank法:")
    print(extractor.extract(text, method='textrank', top_k=5))