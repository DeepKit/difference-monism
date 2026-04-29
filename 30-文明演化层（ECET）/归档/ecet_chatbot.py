"""
ECET AI对话系统 - 快速启动框架
基于偏差反馈优化的对话系统

依赖安装:
    pip install fastapi uvicorn openai

运行:
    python ecet_chatbot.py
"""

import random
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
import json

# ============== 数据模型 ==============
@dataclass
class UserFeedback:
    user_id: str
    response_id: str
    rating: int  # 1-5
    timestamp: datetime

@dataclass
class Response:
    response_id: str
    text: str
    bias_level: float
    creativity_score: float
    timestamp: datetime

# ============== 约束管理器 ==============
class ConstraintManager:
    def __init__(self, max_length=500, style="friendly"):
        self.max_length = max_length
        self.style = style
        self.word_count_history = []
    
    def check(self, text: str) -> bool:
        """检查约束是否满足"""
        word_count = len(text.split())
        self.word_count_history.append(word_count)
        
        # 长度约束
        if word_count > self.max_length:
            return False
        
        return True
    
    def filter(self, text: str) -> str:
        """过滤和截断"""
        words = text.split()
        if len(words) > self.max_length:
            words = words[:self.max_length]
        return " ".join(words)

# ============== 偏差控制器 ==============
class BiasController:
    def __init__(self, initial_temp=0.7, min_temp=0.3, max_temp=1.5):
        self.temperature = initial_temp
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.adaptation_rate = 0.05
        self.history = []
    
    def get_bias_level(self) -> float:
        """获取当前偏差水平"""
        return self.temperature
    
    def adjust(self, recent_feedback: List[UserFeedback]):
        """根据反馈调整偏差"""
        if not recent_feedback:
            return self.temperature
        
        # 计算平均评分
        avg_rating = sum(f.rating for f in recent_feedback) / len(recent_feedback)
        
        # 评分高于3.5 -> 增加偏差（探索更多）
        # 评分低于2.5 -> 减少偏差（保守）
        if avg_rating >= 4.0:
            self.temperature = min(self.max_temp, self.temperature + self.adaptation_rate)
        elif avg_rating <= 2.5:
            self.temperature = max(self.min_temp, self.temperature - self.adaptation_rate)
        
        self.history.append({
            'temperature': self.temperature,
            'avg_rating': avg_rating
        })
        
        return self.temperature

# ============== 反馈闭环系统 ==============
class FeedbackLoop:
    def __init__(self, window_size=10):
        self.feedback_history: List[UserFeedback] = []
        self.response_history: List[Response] = []
        self.window_size = window_size
    
    def add_feedback(self, feedback: UserFeedback):
        """添加反馈"""
        self.feedback_history.append(feedback)
    
    def add_response(self, response: Response):
        """添加响应记录"""
        self.response_history.append(response)
    
    def get_recent_feedback(self, n: int = None) -> List[UserFeedback]:
        """获取最近n条反馈"""
        n = n or self.window_size
        return self.feedback_history[-n:]
    
    def get_diversity_score(self) -> float:
        """计算响应多样性"""
        if len(self.response_history) < 2:
            return 0.0
        
        # 简化版本：基于响应长度的变化
        lengths = [len(r.text) for r in self.response_history[-10:]]
        if not lengths:
            return 0.0
        
        avg_length = sum(lengths) / len(lengths)
        variance = sum((x - avg_length) ** 2 for x in lengths) / len(lengths)
        
        # 归一化到0-1
        diversity = min(1.0, variance / 10000)
        return diversity
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        if not self.feedback_history:
            return {}
        
        recent = self.get_recent_feedback()
        avg_rating = sum(f.rating for f in recent) / len(recent)
        
        return {
            'total_responses': len(self.response_history),
            'total_feedback': len(self.feedback_history),
            'recent_avg_rating': avg_rating,
            'diversity_score': self.get_diversity_score()
        }

# ============== ECET对话系统 ==============
class ECETChatbot:
    def __init__(self):
        self.constraints = ConstraintManager()
        self.bias_controller = BiasController()
        self.feedback_loop = FeedbackLoop()
        self.response_count = 0
    
    def generate_response(self, user_input: str) -> Response:
        """生成响应"""
        self.response_count += 1
        response_id = f"resp_{self.response_count}"
        
        # 获取当前偏差水平
        bias_level = self.bias_controller.get_bias_level()
        
        # 模拟LLM生成（实际项目中替换为真实API调用）
        # 这里用随机响应模拟
        responses = [
            f"关于'{user_input}'，我有一些有趣的想法...",
            f"这是一个很好的问题。让我来分析一下...",
            f"从不同角度来看，{user_input}可以理解为...",
            f"实际上，{user_input}涉及到一个更深刻的问题...",
            f"让我用一个比喻来说明'{user_input}'..."
        ]
        
        # 根据偏差水平选择响应风格
        if bias_level > 1.0:
            # 高偏差：更创新
            text = responses[-1]  # 选择最独特的
        else:
            # 低偏差：更保守
            text = responses[0]
        
        # 检查约束
        if not self.constraints.check(text):
            text = self.constraints.filter(text)
        
        # 计算创造力得分（简化版）
        creativity = bias_level * 0.5 + random.random() * 0.5
        
        response = Response(
            response_id=response_id,
            text=text,
            bias_level=bias_level,
            creativity_score=creativity,
            timestamp=datetime.now()
        )
        
        self.feedback_loop.add_response(response)
        
        return response
    
    def collect_feedback(self, user_id: str, response_id: str, rating: int):
        """收集用户反馈"""
        feedback = UserFeedback(
            user_id=user_id,
            response_id=response_id,
            rating=rating,
            timestamp=datetime.now()
        )
        self.feedback_loop.add_feedback(feedback)
        
        # 调整偏差
        recent = self.feedback_loop.get_recent_feedback()
        self.bias_controller.adjust(recent)
    
    def get_status(self) -> dict:
        """获取系统状态"""
        stats = self.feedback_loop.get_stats()
        stats['current_temperature'] = self.bias_controller.temperature
        return stats

# ============== 模拟运行 ==============
def simulate_conversation():
    """模拟对话流程"""
    bot = ECETChatbot()
    
    print("=" * 50)
    print("ECET AI对话系统 - 模拟运行")
    print("=" * 50)
    
    # 模拟用户输入
    user_inputs = [
        "什么是创新?",
        "如何提高创造力?",
        "为什么有时候努力没有回报?",
        "人工智能会取代人类吗?",
        "生命的意义是什么?"
    ]
    
    for i, user_input in enumerate(user_inputs):
        print(f"\n【用户】{user_input}")
        
        # 生成响应
        response = bot.generate_response(user_input)
        print(f"【AI】{response.text}")
        print(f"   [偏差水平: {response.bias_level:.2f}, 创造力: {response.creativity_score:.2f}]")
        
        # 模拟用户反馈（随机评分）
        rating = random.randint(1, 5)
        bot.collect_feedback(f"user_{i}", response.response_id, rating)
        print(f"   [用户评分: {rating}/5]")
    
    # 打印统计
    print("\n" + "=" * 50)
    print("系统统计")
    print("=" * 50)
    stats = bot.get_status()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 打印偏差历史
    print("\n偏差调整历史:")
    for h in bot.bias_controller.history[-5:]:
        print(f"  temperature: {h['temperature']:.2f}, avg_rating: {h['avg_rating']:.2f}")

if __name__ == "__main__":
    simulate_conversation()
