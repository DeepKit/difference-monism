from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

class SentimentAnalyzer:
    def __init__(self):
        """初始化情感分析器"""
        try:
            self.sia = SentimentIntensityAnalyzer()
        except LookupError:
            nltk.download('vader_lexicon')
            self.sia = SentimentIntensityAnalyzer()
    
    def analyze(self, text):
        """
        分析文本情感
        
        Args:
            text (str): 要分析的文本
            
        Returns:
            dict: 包含neg, neu, pos, compound的情感分数
        """
        if not text or not isinstance(text, str):
            return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
        
        return self.sia.polarity_scores(text)
    
    def get_sentiment(self, text):
        """
        获取文本的情感分类
        
        Args:
            text (str): 要分析的文本
            
        Returns:
            str: 'positive', 'negative', 或 'neutral'
        """
        scores = self.analyze(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            return 'positive'
        elif compound <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def batch_analyze(self, texts):
        """
        批量分析多个文本
        
        Args:
            texts (list): 文本列表
            
        Returns:
            list: 每个文本的情感分数列表
        """
        return [self.analyze(text) for text in texts]


# 使用示例
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # 单个文本分析
    text1 = "I love this product! It's amazing!"
    print(f"文本: {text1}")
    print(f"分数: {analyzer.analyze(text1)}")
    print(f"情感: {analyzer.get_sentiment(text1)}\n")
    
    text2 = "This is terrible. I hate it."
    print(f"文本: {text2}")
    print(f"分数: {analyzer.analyze(text2)}")
    print(f"情感: {analyzer.get_sentiment(text2)}\n")
    
    # 批量分析
    texts = [
        "Great experience!",
        "Not bad, could be better.",
        "Worst purchase ever."
    ]
    results = analyzer.batch_analyze(texts)
    for text, result in zip(texts, results):
        print(f"{text}: {result}")