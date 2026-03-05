from typing import Dict, List, Optional, Tuple
from collections import Counter
import re


class LanguageDetector:
    """语言检测器类"""
    
    def __init__(self):
        # 常见语言的特征字符集
        self.language_patterns = {
            'zh': r'[\u4e00-\u9fff]',  # 中文
            'ja': r'[\u3040-\u309f\u30a0-\u30ff]',  # 日文
            'ko': r'[\uac00-\ud7af]',  # 韩文
            'ar': r'[\u0600-\u06ff]',  # 阿拉伯文
            'ru': r'[\u0400-\u04ff]',  # 俄文
            'el': r'[\u0370-\u03ff]',  # 希腊文
            'th': r'[\u0e00-\u0e7f]',  # 泰文
        }
        
        # 常见英文停用词
        self.en_stopwords = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but'}
        
        # 常见其他语言停用词示例
        self.stopwords = {
            'es': {'el', 'la', 'de', 'que', 'y', 'en', 'un', 'ser', 'se', 'no'},
            'fr': {'le', 'de', 'un', 'être', 'et', 'à', 'il', 'avoir', 'ne', 'je'},
            'de': {'der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich'},
            'pt': {'o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para'},
            'it': {'il', 'di', 'e', 'la', 'che', 'per', 'un', 'in', 'è', 'a'},
        }
    
    def detect(self, text: str) -> str:
        """检测文本语言"""
        if not text or not text.strip():
            return 'unknown'
        
        result = self.detect_with_confidence(text)
        return result[0]
    
    def detect_with_confidence(self, text: str) -> Tuple[str, float]:
        """检测文本语言并返回置信度"""
        if not text or not text.strip():
            return ('unknown', 0.0)
        
        text = text.strip()
        scores = {}
        
        # 检查特殊字符集
        for lang, pattern in self.language_patterns.items():
            matches = len(re.findall(pattern, text))
            if matches > 0:
                scores[lang] = matches / len(text)
        
        # 如果找到明显的非拉丁字符语言
        if scores:
            best_lang = max(scores.items(), key=lambda x: x[1])
            if best_lang[1] > 0.3:  # 超过30%的字符匹配
                return (best_lang[0], best_lang[1])
        
        # 检查拉丁字母语言
        words = re.findall(r'\b[a-zA-Zàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]+\b', text.lower())
        
        if not words:
            return ('unknown', 0.0)
        
        # 英文检测
        en_matches = sum(1 for word in words if word in self.en_stopwords)
        if en_matches > 0:
            scores['en'] = en_matches / len(words)
        
        # 其他语言检测
        for lang, stopwords in self.stopwords.items():
            matches = sum(1 for word in words if word in stopwords)
            if matches > 0:
                scores[lang] = matches / len(words)
        
        if not scores:
            # 默认返回英文
            return ('en', 0.5)
        
        best_lang = max(scores.items(), key=lambda x: x[1])
        return (best_lang[0], min(best_lang[1], 1.0))
    
    def detect_multiple(self, texts: List[str]) -> List[str]:
        """批量检测多个文本的语言"""
        return [self.detect(text) for text in texts]
    
    def get_language_stats(self, text: str) -> Dict[str, float]:
        """获取文本中各语言的统计信息"""
        if not text or not text.strip():
            return {}
        
        stats = {}
        
        # 统计特殊字符集
        for lang, pattern in self.language_patterns.items():
            matches = len(re.findall(pattern, text))
            if matches > 0:
                stats[lang] = matches / len(text)
        
        # 统计拉丁字母语言
        words = re.findall(r'\b[a-zA-Zàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]+\b', text.lower())
        
        if words:
            en_matches = sum(1 for word in words if word in self.en_stopwords)
            if en_matches > 0:
                stats['en'] = en_matches / len(words)
            
            for lang, stopwords in self.stopwords.items():
                matches = sum(1 for word in words if word in stopwords)
                if matches > 0:
                    stats[lang] = matches / len(words)
        
        return stats


# 使用示例
if __name__ == '__main__':
    detector = LanguageDetector()
    
    # 测试用例
    test_texts = [
        "Hello, how are you today?",
        "你好，今天天气怎么样？",
        "こんにちは、元気ですか？",
        "Bonjour, comment allez-vous?",
        "Hola, ¿cómo estás?",
        "Привет, как дела?",
    ]
    
    for text in test_texts:
        lang, confidence = detector.detect_with_confidence(text)
        print(f"Text: {text[:30]}...")
        print(f"Language: {lang}, Confidence: {confidence:.2f}\n")