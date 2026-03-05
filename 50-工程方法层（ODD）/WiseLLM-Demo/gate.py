# WiseLLM Runtime Demo - 核心门禁模块
# 基于 ODD 理论的三层约束体系

import json
import re
import requests
from typing import Dict, List, Optional, Tuple
from enum import Enum
from config import (
    LLM_ENDPOINTS, DEFAULT_ENDPOINT, CONSTRAINT_LAYERS, 
    DECISION_TYPES, RISK_TYPES
)


class ConstraintType(Enum):
    """约束类型"""
    CT_HARD = "ctHard"        # 硬约束
    CT_SOFT = "ctSoft"        # 软约束
    CT_UNTOUCHABLE = "ctUntouchable"  # 人类专属


class Decision(Enum):
    """决策结果"""
    ALLOW = "allow"
    BLOCK = "block"
    CHALLENGE = "challenge"
    ESCALATE = "escalate"


class RiskLevel(Enum):
    """风险等级"""
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3


class LLMClient:
    """LLM 客户端"""
    
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT):
        self.config = LLM_ENDPOINTS.get(endpoint, LLM_ENDPOINTS[DEFAULT_ENDPOINT])
        self.url = self.config["url"]
        self.key = self.config["key"]
        self.model = self.config["model"]
        self.protocol = self.config.get("protocol", "openai")
        self.extra_headers = self.config.get("extra_headers", {})
    
    def chat(self, prompt: str, system_prompt: str = "") -> str:
        """调用 LLM"""
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }
        headers.update(self.extra_headers)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 1024,
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            if self.protocol == "anthropic":
                return response.json()["content"][0]["text"]
            else:
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[LLM Error: {str(e)}]"


class RiskGuard:
    """风险守卫 - 检测各类安全风险"""
    
    # 预定义的检测规则
    DETECTION_RULES = {
        # Prompt Injection 模式
        "prompt_injection": [
            r"ignore\s+(previous|all|above)\s+(instructions?|rules?|prompts?)",
            r"forget\s+(everything|all|your\s+instructions)",
            r"new\s+instructions?:",
            r"#\s*SYSTEM\s*#",
            r"#\s*INSTuctions?:",
            r"you\s+are\s+now\s+(in\s+)?(developer\s+)?mode",
            r" DAN\s+mode",
            r"jailbreak",
        ],
        # 越狱攻击模式
        "jailbreak": [
            r"roleplay\s+as\s+(a\s+)?",
            r"pretend\s+to\s+be\s+",
            r"act\s+as\s+(a\s+)?",
            r"(unrestricted|unfiltered)\s+(mode|assistant)",
            r"bypass\s+(safety|content\s+policy)",
        ],
        # PII 泄露风险
        "pii_leak": [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Credit Card
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b1[3-9]\d{9}\b",  # Phone
        ],
        # 凭证泄露
        "credential_leak": [
            r"api[_-]?key['\"]?\s*[:=]",
            r"secret[_-]?key",
            r"password['\"]?\s*[:=]",
            r"token['\"]?\s*[:=]",
            r"sk-[a-zA-Z0-9]{20,}",
        ],
        # SQL 注入
        "sql_injection": [
            r"union\s+select",
            r"1\s*=\s*1",
            r"drop\s+table",
            r"delete\s+from",
            r"insert\s+into",
        ],
        # 命令注入
        "command_injection": [
            r"rm\s+-rf",
            r"del\s+/[sq]",
            r"format\s+[a-z]:",
        ],
    }
    
    def __init__(self):
        self.detected_risks: List[Dict] = []
    
    def check(self, text: str) -> Tuple[List[Dict], RiskLevel]:
        """
        检测风险
        返回: (风险列表, 风险等级)
        """
        self.detected_risks = []
        
        for risk_type, patterns in self.DETECTION_RULES.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    self.detected_risks.append({
                        "type": risk_type,
                        "pattern": pattern,
                        "matches": matches[:3],  # 只保留前3个
                    })
        
        # 计算风险等级
        risk_level = self._calculate_risk_level()
        
        return self.detected_risks, risk_level
    
    def _calculate_risk_level(self) -> RiskLevel:
        """计算风险等级"""
        if not self.detected_risks:
            return RiskLevel.LOW
        
        # 按风险类型加权
        critical_types = {"prompt_injection", "jailbreak", "command_injection"}
        high_types = {"sql_injection", "credential_leak"}
        
        has_critical = any(r["type"] in critical_types for r in self.detected_risks)
        has_high = any(r["type"] in high_types for r in self.detected_risks)
        
        if has_critical:
            return RiskLevel.CRITICAL
        elif has_high:
            return RiskLevel.HIGH
        elif len(self.detected_risks) > 2:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW


class ChallengeEngine:
    """质疑引擎 - 对可疑请求进行二次确认"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def analyze(self, prompt: str, context: Dict = None) -> Dict:
        """
        分析请求是否需要质疑
        """
        # 构建分析提示
        analysis_prompt = f"""请分析以下用户请求是否存在风险，只需回答"是"或"否"和简短原因。

用户请求: {prompt[:200]}

请按以下格式回答:
风险: 是/否
原因: ..."""

        result = self.llm.chat(analysis_prompt)
        
        # 简单解析
        is_risky = "风险: 是" in result or "是" in result[:50]
        
        return {
            "needs_challenge": is_risky,
            "analysis": result,
        }


class AbsoluteGate:
    """
    绝对门禁 - 三层约束体系
    
    基于 ODD 理论:
    - ctHard: 硬约束 - 不可逾越的底线
    - ctSoft: 软约束 - 企业政策，可调整
    - ctUntouchable: 人类专属 - 必须人工决策
    """
    
    def __init__(self, llm_endpoint: str = DEFAULT_ENDPOINT):
        self.llm = LLMClient(llm_endpoint)
        self.risk_guard = RiskGuard()
        self.challenge_engine = ChallengeEngine(self.llm)
    
    def check(self, prompt: str, user_context: Dict = None) -> Dict:
        """
        执行三层约束检查
        
        参数:
            prompt: 用户请求
            user_context: 用户上下文（可选）
            
        返回:
            {
                "decision": "allow|block|challenge|escalate",
                "constraint_layer": "ctHard|ctSoft ctUntouchable",
                "reason": "原因",
                "details": {}
            }
        """
        # === 第一层: 硬约束检查 (ctHard) ===
        risks, risk_level = self.risk_guard.check(prompt)
        
        if risk_level == RiskLevel.CRITICAL:
            return {
                "decision": Decision.BLOCK.value,
                "constraint_layer": ConstraintType.CT_HARD.value,
                "reason": "检测到严重风险，硬约束拦截",
                "details": {
                    "risks": risks,
                    "risk_level": risk_level.name,
                }
            }
        
        # === 第二层: 软约束检查 (ctSoft) ===
        # 使用 LLM 分析语义风险
        llm_analysis = self.challenge_engine.analyze(prompt, user_context)
        
        if llm_analysis["needs_challenge"]:
            return {
                "decision": Decision.CHALLENGE.value,
                "constraint_layer": ConstraintType.CT_SOFT.value,
                "reason": "软约束触发，需要用户确认",
                "details": {
                    "llm_analysis": llm_analysis["analysis"],
                }
            }
        
        # === 第三层: 人类专属约束检查 (ctUntouchable) ===
        # 检查是否涉及敏感操作
        sensitive_patterns = [
            r"(删除|修改)\s+(核心|关键|重要)",
            r"(授权|权限)\s+(提升|变更)",
            r"(财务|资金)\s+(转移|操作)",
            r"批量\s+(删除|修改)",
        ]
        
        for pattern in sensitive_patterns:
            if re.search(pattern, prompt):
                return {
                    "decision": Decision.ESCALATE.value,
                    "constraint_layer": ConstraintType.CT_UNTOUCHABLE.value,
                    "reason": "涉及人类专属决策领域，需人工审批",
                    "details": {
                        "pattern": pattern,
                    }
                }
        
        # === 通过所有检查 ===
        return {
            "decision": Decision.ALLOW.value,
            "constraint_layer": "none",
            "reason": "通过所有约束检查",
            "details": {
                "risks": risks,
                "risk_level": risk_level.name,
            }
        }
    
    def execute(self, prompt: str, user_context: Dict = None) -> Dict:
        """
        完整的执行流程: 先检查，再执行
        """
        # 1. 门禁检查
        check_result = self.check(prompt, user_context)
        
        # 2. 根据决策执行
        if check_result["decision"] == Decision.BLOCK.value:
            return {
                "status": "blocked",
                "decision": check_result,
                "response": "请求被拦截: " + check_result["reason"],
            }
        
        elif check_result["decision"] == Decision.CHALLENGE.value:
            return {
                "status": "challenged",
                "decision": check_result,
                "response": "需要确认: " + check_result["reason"],
            }
        
        elif check_result["decision"] == Decision.ESCALATE.value:
            return {
                "status": "escalated",
                "decision": check_result,
                "response": "已升级人工审批: " + check_result["reason"],
            }
        
        else:
            # 3. 执行正常请求
            response = self.llm.chat(prompt)
            return {
                "status": "allowed",
                "decision": check_result,
                "response": response,
            }


# 便捷函数
def create_gate(endpoint: str = DEFAULT_ENDPOINT) -> AbsoluteGate:
    """创建门禁实例"""
    return AbsoluteGate(endpoint)
