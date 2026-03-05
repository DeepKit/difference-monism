from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

class SentimentAnalyzer:
    def __init__(self):
        try:
            self.sia = SentimentIntensityAnalyzer()
        except LookupError:
            nltk.download('vader_lexicon')
            self.sia = SentimentIntensityAnalyzer()
    
    def analyze(self, text):
        """
        分析文本情感
        返回: {'neg': 负面, 'neu': 中性, 'pos': 正面, 'compound': 综合得分}
        """
        return self.sia.polarity_scores(text)
    
    def get_sentiment(self, text):
        """
        获取情感标签: 'positive', 'negative', 'neutral'
        """
        score = self.analyze(text)['compound']
        if score >= 0.05:
            return 'positive'
        elif score <= -0.05:
            return 'negative'
        return 'neutral'


# 使用示例
analyzer = SentimentAnalyzer()
print(analyzer.analyze("I love this product!"))
print(analyzer.get_sentiment("This is terrible"))