from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class TextSimilarity:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.vectors = None
        self.texts = []
    
    def fit(self, texts):
        """训练文本向量化模型"""
        self.texts = texts
        self.vectors = self.vectorizer.fit_transform(texts)
        return self
    
    def cosine_similarity(self, text1, text2):
        """计算两个文本的余弦相似度"""
        vectors = self.vectorizer.transform([text1, text2])
        return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    
    def jaccard_similarity(self, text1, text2):
        """计算两个文本的Jaccard相似度"""
        set1 = set(text1.split())
        set2 = set(text2.split())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0
    
    def find_most_similar(self, query, top_k=5):
        """找到与查询文本最相似的文本"""
        if not self.texts:
            return []
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        return [(self.texts[i], similarities[i]) for i in top_indices]


# 使用示例
if __name__ == "__main__":
    texts = [
        "机器学习是人工智能的一个分支",
        "深度学习是机器学习的子领域",
        "今天天气很好",
        "自然语言处理属于人工智能"
    ]
    
    sim = TextSimilarity()
    sim.fit(texts)
    
    # 余弦相似度
    score = sim.cosine_similarity("机器学习很有趣", "深度学习很强大")
    print(f"余弦相似度: {score:.4f}")
    
    # Jaccard相似度
    score = sim.jaccard_similarity("机器学习很有趣", "深度学习很强大")
    print(f"Jaccard相似度: {score:.4f}")
    
    # 查找最相似文本
    results = sim.find_most_similar("人工智能和机器学习", top_k=3)
    print("\n最相似的文本:")
    for text, score in results:
        print(f"  {text} (相似度: {score:.4f})")