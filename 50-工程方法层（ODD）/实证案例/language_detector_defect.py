from langdetect import detect, detect_langs
from typing import List, Dict

class LanguageDetector:
    """简洁的语言检测类"""
    
    def detect(self, text: str) -> str:
        """检测文本语言，返回语言代码"""
        try:
            return detect(text)
        except:
            return "unknown"
    
    def detect_with_confidence(self, text: str) -> List[Dict[str, float]]:
        """检测语言并返回置信度"""
        try:
            results = detect_langs(text)
            return [{"lang": r.lang, "prob": r.prob} for r in results]
        except:
            return []
    
    def is_language(self, text: str, target_lang: str) -> bool:
        """判断文本是否为指定语言"""
        return self.detect(text) == target_lang


# 使用示例
if __name__ == "__main__":
    detector = LanguageDetector()
    
    print(detector.detect("Hello world"))  # en
    print(detector.detect("你好世界"))      # zh-cn
    print(detector.detect_with_confidence("Bonjour le monde"))
    print(detector.is_language("こんにちは", "ja"))