# WiseLLM Runtime Demo - 配置文件
# 基于 ODD 理论的三层约束体系

LLM_ENDPOINTS = {
    "kiro": {
        "url": "http://localhost:8000/v1/chat/completions",
        "key": "fuyi-kiro-17781158558",
        "model": "claude-opus-4-6",
    },
    "duojie": {
        "url": "https://api.duojie.games/v1/messages",
        "key": "sk-hXbs2jQOon47kB49GDhcwFONRhEhCB8Q7DnEuvLB2M74ARg9",
        "model": "claude-opus-4-6-kiro",
        "protocol": "anthropic",
    },
    "iflow": {
        "url": "https://apis.iflow.cn/v1/chat/completions",
        "key": "sk-b912a6d7a0b22087228dfaafed4ff9c4",
        "model": "kimi-k2.5",
        "extra_headers": {"user-agent": "iFlow-Cli"},
    },
    "augment": {
        "url": "https://augment.net.cn/v1/chat/completions",
        "key": "sk-cMsIWftc1Fyia3Iz3vHBgd6SnONHOQIk",
        "model": "qwen3.5-397b-a17b",
    },
}

# 默认使用 Kiro
DEFAULT_ENDPOINT = "kiro"

# 三层约束配置
CONSTRAINT_LAYERS = {
    "ctHard": {
        "name": "硬约束",
        "description": "不可逾越的底线，如法律法规、伦理红线",
        "priority": 1,
    },
    "ctSoft": {
        "name": "软约束",
        "description": "企业政策、最佳实践，可根据场景调整",
        "priority": 2,
    },
    "ctUntouchable": {
        "name": "人类专属约束",
        "description": "必须由人类决策的领域，如重大权限变更",
        "priority": 3,
    },
}

# 决策类型
DECISION_TYPES = {
    "allow": {"code": 0, "message": "允许执行"},
    "block": {"code": 1, "message": "拦截"},
    "challenge": {"code": 2, "message": "质疑，需要确认"},
    "escalate": {"code": 3, "message": "升级，需人工审批"},
}

# 风险类型
RISK_TYPES = [
    "prompt_injection",
    "jailbreak",
    "pii_leak",
    "credential_leak",
    "sql_injection",
    "command_injection",
    "越权操作",
    "敏感数据请求",
]
