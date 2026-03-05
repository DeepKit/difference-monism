from sklearn.feature_extraction.text import TfidfVectorizer
import re
from typing import List, Tuple

class KeywordExtractor:
    def __init__(self, max_features: int = 100, ngram_range: Tuple[int, int] = (1, 2)):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            stop_words='english',
            lowercase=True
        )
    
    def extract(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """从单个文本提取关键词"""
        cleaned = self._clean_text(text)
        tfidf_matrix = self.vectorizer.fit_transform([cleaned])
        feature_names = self.vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        keywords = [(feature_names[i], scores[i]) for i in range(len(scores))]
        keywords.sort(key=lambda x: x[1], reverse=True)
        return keywords[:top_n]
    
    def extract_batch(self, texts: List[str], top_n: int = 10) -> List[List[Tuple[str, float]]]:
        """从多个文本提取关键词"""
        cleaned_texts = [self._clean_text(t) for t in texts]
        tfidf_matrix = self.vectorizer.fit_transform(cleaned_texts)
        feature_names = self.vectorizer.get_feature_names_out()
        
        results = []
        for i in range(len(texts)):
            scores = tfidf_matrix.toarray()[i]
            keywords = [(feature_names[j], scores[j]) for j in range(len(scores))]
            keywords.sort(key=lambda x: x[1], reverse=True)
            results.append(keywords[:top_n])
        return results
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


# 使用示例
if __name__ == "__main__":
    extractor = KeywordExtractor()
    
    text = "Python is a high-level programming language. Python is widely used for data science and machine learning."
    keywords = extractor.extract(text, top_n=5)
    
    for word, score in keywords:
        print(f"{word}: {score:.4f}")