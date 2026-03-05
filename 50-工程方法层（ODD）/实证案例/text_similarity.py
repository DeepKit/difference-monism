"""
文本相似度计算类
支持多种相似度算法和文本预处理方法
"""

from typing import List, Tuple, Optional, Union
import re
import math
from collections import Counter
from difflib import SequenceMatcher
import warnings


class TextSimilarity:
    """文本相似度计算工具类"""
    
    def __init__(self, method: str = "cosine", case_sensitive: bool = False):
        """
        初始化文本相似度计算器
        
        Args:
            method: 相似度计算方法 ('cosine', 'jaccard', 'levenshtein', 'jaro_winkler')
            case_sensitive: 是否区分大小写
        """
        self.method = method.lower()
        self.case_sensitive = case_sensitive
        
        valid_methods = ['cosine', 'jaccard', 'levenshtein', 'jaro_winkler', 'dice']
        if self.method not in valid_methods:
            raise ValueError(f"不支持的方法: {method}. 支持的方法: {valid_methods}")
    
    def preprocess(self, text: str) -> str:
        """
        文本预处理
        
        Args:
            text: 输入文本
            
        Returns:
            预处理后的文本
        """
        if not isinstance(text, str):
            raise TypeError(f"输入必须是字符串类型，当前类型: {type(text)}")
        
        if not self.case_sensitive:
            text = text.lower()
        
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        文本分词
        
        Args:
            text: 输入文本
            
        Returns:
            分词列表
        """
        text = self.preprocess(text)
        
        # 简单的分词策略：按空格和标点分割
        tokens = re.findall(r'\w+', text)
        
        return tokens if tokens else []
    
    def cosine_similarity(self, text1: str, text2: str) -> float:
        """
        余弦相似度计算
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度分数 [0, 1]
        """
        try:
            tokens1 = self.tokenize(text1)
            tokens2 = self.tokenize(text2)
            
            if not tokens1 or not tokens2:
                return 0.0
            
            # 构建词频向量
            counter1 = Counter(tokens1)
            counter2 = Counter(tokens2)
            
            # 获取所有唯一词
            all_tokens = set(counter1.keys()) | set(counter2.keys())
            
            # 计算向量点积和模
            dot_product = sum(counter1[token] * counter2[token] for token in all_tokens)
            magnitude1 = math.sqrt(sum(count ** 2 for count in counter1.values()))
            magnitude2 = math.sqrt(sum(count ** 2 for count in counter2.values()))
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return dot_product / (magnitude1 * magnitude2)
        
        except Exception as e:
            warnings.warn(f"余弦相似度计算错误: {str(e)}")
            return 0.0
    
    def jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Jaccard相似度计算
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度分数 [0, 1]
        """
        try:
            tokens1 = set(self.tokenize(text1))
            tokens2 = set(self.tokenize(text2))
            
            if not tokens1 and not tokens2:
                return 1.0
            
            if not tokens1 or not tokens2:
                return 0.0
            
            intersection = tokens1 & tokens2
            union = tokens1 | tokens2
            
            return len(intersection) / len(union)
        
        except Exception as e:
            warnings.warn(f"Jaccard相似度计算错误: {str(e)}")
            return 0.0
    
    def levenshtein_distance(self, text1: str, text2: str) -> int:
        """
        计算Levenshtein编辑距离
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            编辑距离
        """
        try:
            s1 = self.preprocess(text1)
            s2 = self.preprocess(text2)
            
            if len(s1) < len(s2):
                s1, s2 = s2, s1
            
            if len(s2) == 0:
                return len(s1)
            
            previous_row = range(len(s2) + 1)
            
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            
            return previous_row[-1]
        
        except Exception as e:
            warnings.warn(f"Levenshtein距离计算错误: {str(e)}")
            return max(len(text1), len(text2))
    
    def levenshtein_similarity(self, text1: str, text2: str) -> float:
        """
        基于Levenshtein距离的相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度分数 [0, 1]
        """
        try:
            distance = self.levenshtein_distance(text1, text2)
            max_len = max(len(self.preprocess(text1)), len(self.preprocess(text2)))
            
            if max_len == 0:
                return 1.0
            
            return 1 - (distance / max_len)
        
        except Exception as e:
            warnings.warn(f"Levenshtein相似度计算错误: {str(e)}")
            return 0.0
    
    def jaro_winkler_similarity(self, text1: str, text2: str, prefix_scale: float = 0.1) -> float:
        """
        Jaro-Winkler相似度计算
        
        Args:
            text1: 文本1
            text2: 文本2
            prefix_scale: 前缀权重
            
        Returns:
            相似度分数 [0, 1]
        """
        try:
            s1 = self.preprocess(text1)
            s2 = self.preprocess(text2)
            
            if s1 == s2:
                return 1.0
            
            if not s1 or not s2:
                return 0.0
            
            # Jaro相似度
            match_distance = max(len(s1), len(s2)) // 2 - 1
            match_distance = max(0, match_distance)
            
            s1_matches = [False] * len(s1)
            s2_matches = [False] * len(s2)
            
            matches = 0
            transpositions = 0
            
            for i in range(len(s1)):
                start = max(0, i - match_distance)
                end = min(i + match_distance + 1, len(s2))
                
                for j in range(start, end):
                    if s2_matches[j] or s1[i] != s2[j]:
                        continue
                    s1_matches[i] = True
                    s2_matches[j] = True
                    matches += 1
                    break
            
            if matches == 0:
                return 0.0
            
            k = 0
            for i in range(len(s1)):
                if not s1_matches[i]:
                    continue
                while not s2_matches[k]:
                    k += 1
                if s1[i] != s2[k]:
                    transpositions += 1
                k += 1
            
            jaro = (matches / len(s1) + matches / len(s2) + 
                   (matches - transpositions / 2) / matches) / 3
            
            # Jaro-Winkler调整
            prefix_len = 0
            for i in range(min(len(s1), len(s2), 4)):
                if s1[i] == s2[i]:
                    prefix_len += 1
                else:
                    break
            
            return jaro + prefix_len * prefix_scale * (1 - jaro)
        
        except Exception as e:
            warnings.warn(f"Jaro-Winkler相似度计算错误: {str(e)}")
            return 0.0
    
    def dice_coefficient(self, text1: str, text2: str) -> float:
        """
        Dice系数计算
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            相似度分数 [0, 1]
        """
        try:
            tokens1 = self.tokenize(text1)
            tokens2 = self.tokenize(text2)
            
            if not tokens1 and not tokens2:
                return 1.0
            
            if not tokens1 or not tokens2:
                return 0.0
            
            set1 = set(tokens1)
            set2 = set(tokens2)
            
            intersection = set1 & set2
            
            return 2 * len(intersection) / (len(set1) + len(set2))
        
        except Exception as e:
            warnings.warn(f"Dice系数计算错误: {str(e)}")
            return 0.0
    
    def similarity(self, text1: str, text2: str, method: Optional[str] = None) -> float:
        """
        计算文本相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            method: 指定计算方法，如果为None则使用初始化时的方法
            
        Returns:
            相似度分数 [0, 1]
        """
        if not isinstance(text1, str) or not isinstance(text2, str):
            raise TypeError("输入必须是字符串类型")
        
        method = method.lower() if method else self.method
        
        method_map = {
            'cosine': self.cosine_similarity,
            'jaccard': self.jaccard_similarity,
            'levenshtein': self.levenshtein_similarity,
            'jaro_winkler': self.jaro_winkler_similarity,
            'dice': self.dice_coefficient
        }
        
        if method not in method_map:
            raise ValueError(f"不支持的方法: {method}")
        
        return method_map[method](text1, text2)
    
    def batch_similarity(self, text: str, text_list: List[str], 
                        top_k: Optional[int] = None) -> List[Tuple[int, float]]:
        """
        批量计算相似度并返回排序结果
        
        Args:
            text: 查询文本
            text_list: 待比较文本列表
            top_k: 返回前k个最相似的结果
            
        Returns:
            [(索引, 相似度分数), ...] 按相似度降序排列
        """
        if not isinstance(text_list, list):
            raise TypeError("text_list必须是列表类型")
        
        results = []
        for idx, candidate in enumerate(text_list):
            try:
                score = self.similarity(text, candidate)
                results.append((idx, score))
            except Exception as e:
                warnings.warn(f"计算索引{idx}的相似度时出错: {str(e)}")
                results.append((idx, 0.0))
        
        # 按相似度降序排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        if top_k is not None and top_k > 0:
            return results[:top_k]
        
        return results
    
    def find_most_similar(self, text: str, text_list: List[str]) -> Tuple[int, float]:
        """
        找到最相似的文本
        
        Args:
            text: 查询文本
            text_list: 待比较文本列表
            
        Returns:
            (最相似文本的索引, 相似度分数)
        """
        if not text_list:
            raise ValueError("text_list不能为空")
        
        results = self.batch_similarity(text, text_list, top_k=1)
        return results[0] if results else (-1, 0.0)


# 使用示例
if __name__ == "__main__":
    # 创建相似度计算器
    sim = TextSimilarity(method="cosine", case_sensitive=False)
    
    # 测试文本
    text1 = "Python是一种高级编程语言"
    text2 = "Python是一门高级的编程语言"
    text3 = "Java是一种面向对象的编程语言"
    
    # 计算相似度
    print(f"余弦相似度: {sim.similarity(text1, text2, 'cosine'):.4f}")
    print(f"Jaccard相似度: {sim.similarity(text1, text2, 'jaccard'):.4f}")
    print(f"Levenshtein相似度: {sim.similarity(text1, text2, 'levenshtein'):.4f}")
    print(f"Jaro-Winkler相似度: {sim.similarity(text1, text2, 'jaro_winkler'):.4f}")
    print(f"Dice系数: {sim.similarity(text1, text2, 'dice'):.4f}")
    
    # 批量比较
    candidates = [text2, text3, "机器学习是人工智能的一个分支"]
    results = sim.batch_similarity(text1, candidates, top_k=2)
    print(f"\n最相似的前2个文本:")
    for idx, score in results:
        print(f"  索引{idx}: {candidates[idx][:20]}... (相似度: {score:.4f})")