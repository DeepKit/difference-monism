# 可用 LLM 端点配置

> **版本**: 1.0
> **更新日期**: 2026-02-20

---

## 1. Kiro Gateway（本地代理）

- **端点**: http://localhost:8000
- **Key**: fuyi-kiro-17781158558
- **协议**: Anthropic + OpenAI 兼容

| 模型名 | 实际模型 | 推荐 |
|--------|----------|------|
| claude-opus-4-6 | Claude Opus 4.6 (原生) | ⭐ 最新 |
| claude-opus-4-5 | Claude Opus 4.5 (原生) | |
| claude-sonnet-4-5 | Claude Sonnet 4.5 (原生) | |
| claude-haiku-4-5 | Claude Haiku 4.5 (原生) | |

---

## 2. duojie（Anthropic 协议）

- **端点**: https://api.duojie.games
- **Key**: sk-hXbs2jQOon47kB49GDhcwFONRhEhCB8Q7DnEuvLB2M74ARg9
- **协议**: Anthropic

| 模型名 | 公司 | 推荐 |
|--------|------|------|
| claude-opus-4-6-kiro | Anthropic | ⭐ 最新 |
| claude-opus-4-5-kiro | Anthropic | |
| claude-sonnet-4-5 | Anthropic | |
| claude-haiku-4-5 | Anthropic | |

---

## 3. iFlow（OpenAI 协议）

- **端点**: https://apis.iflow.cn/v1/chat/completions
- **Key**: sk-b912a6d7a0b22087228dfaafed4ff9c4
- **额外 Header**: user-agent: iFlow-Cli

| 模型名 | 公司 | 推荐 |
|--------|------|------|
| kimi-k2-0905 | Moonshot | ⭐ 最新 |
| kimi-k2.5 | Moonshot | |
| claude4-sonnet | Anthropic | |
| glm-5 | 智谱 | ⭐ 最新 |
| glm-4 | 智谱 | |
| minimax-m2.5 | MiniMax | |

---

## 4. Augment（OpenAI 协议）

- **端点**: https://augment.net.cn/v1/chat/completions
- **Key**: sk-cMsIWftc1Fyia3Iz3vHBgd6SnONHOQIk

| 模型名 | 公司 | 推荐 |
|--------|------|------|
| qwen3.5-397b-a17b | 阿里 | ⭐ 最新 |
| kimi-k2.5 | Moonshot | |
| glm-5 | 智谱 | |

---

## 推荐模型选择

### 评测实验推荐

| 用途 | 推荐模型 | 端点 |
|------|----------|------|
| 主测试 | claude-opus-4-6 | Kiro / duojie |
| 对比测试 | kimi-k2-0905 | iFlow |
| 对比测试 | glm-5 | iFlow / Augment |
| 对比测试 | qwen3.5-397b-a17b | Augment |

### curl 示例

**OpenAI 协议（iFlow）**:
```bash
curl https://apis.iflow.cn/v1/chat/completions \
  -H "Authorization: Bearer sk-b912a6d7a0b22087228dfaafed4ff9c4" \
  -H "Content-Type: application/json" \
  -H "user-agent: iFlow-Cli" \
  -d '{"model":"kimi-k2.5","max_tokens":100,"messages":[{"role":"user","content":"你好"}]}'
```

**Anthropic 协议（duojie）**:
```bash
curl https://api.duojie.games/v1/messages \
  -H "x-api-key: sk-hXbs2jQOon47kB49GDhcwFONRhEhCB8Q7DnEuvLB2M74ARg9" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4-6-kiro","max_tokens":100,"messages":[{"role":"user","content":"你好"}]}'
```

**OpenAI 协议（Kiro 本地）**:
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer fuyi-kiro-17781158558" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4-6","max_tokens":100,"messages":[{"role":"user","content":"你好"}]}'
```

---

## 涉及公司

- Anthropic（Claude 系列）
- Moonshot（月之暗面 Kimi）
- 智谱（GLM）
- 阿里（Qwen）
- MiniMax

---

*版本: 1.0 | 更新: 2026-02-20*
