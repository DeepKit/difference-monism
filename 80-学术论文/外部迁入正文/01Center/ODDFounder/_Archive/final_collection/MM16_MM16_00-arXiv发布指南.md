# arXiv 论文发布指南

> 针对 ODD 论文的发布步骤

---

## 1. 注册 arXiv 账号

1. 访问 https://arxiv.org/user/register
2. 填写信息：
   - Email（建议用学术邮箱，如 .edu，审核更快）
   - 姓名、机构（可填公司名或独立研究者）
3. 等待邮件验证（通常几分钟）

**注意**：首次提交需要 endorsement（背书），见第5节。

---

## 2. 准备论文文件

### 2.1 格式要求

| 格式 | 说明 |
|------|------|
| **推荐** | LaTeX（.tex）+ PDF |
| 可接受 | 纯 PDF（但不推荐） |
| 模板 | 使用 arXiv 标准模板或会议模板 |

### 2.2 将 Markdown 转换为 LaTeX

```bash
# 方法1：使用 Pandoc
pandoc 09-ODD-Academic-Paper-EN.md -o ODD-Paper.tex

# 方法2：在线工具
# https://www.markdowntolatex.com/
```

### 2.3 推荐的 LaTeX 模板

```latex
\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{booktabs}

\title{ODD: Output-Driven Development\\
A Novel Methodology for AI-Assisted Software Engineering}
\author{Your Name\\
\texttt{your.email@example.com}}
\date{January 2026}

\begin{document}
\maketitle
\begin{abstract}
...
\end{abstract}
...
\end{document}
```

### 2.4 文件检查清单

- [ ] PDF 可正常打开
- [ ] 所有图片已嵌入
- [ ] 参考文献格式正确
- [ ] 无编译错误/警告
- [ ] 文件大小 < 50MB

---

## 3. 选择分类（Category）

ODD 论文推荐分类：

| 分类代码 | 名称 | 适合度 |
|----------|------|:------:|
| **cs.SE** | Software Engineering | ★★★★★ |
| cs.AI | Artificial Intelligence | ★★★★ |
| cs.HC | Human-Computer Interaction | ★★★ |
| cs.PL | Programming Languages | ★★★ |

**主分类**：`cs.SE`（软件工程）
**交叉分类**：`cs.AI`（可选）

---

## 4. 提交流程

### 4.1 登录并开始提交

1. 登录 https://arxiv.org
2. 点击 "Submit" 按钮
3. 选择 "New Submission"

### 4.2 填写元数据

```
Title: ODD: Output-Driven Development - A Novel Methodology 
       for AI-Assisted Software Engineering

Authors: [Your Name]

Abstract: [复制论文摘要]

Comments: 15 pages, 5 tables, preprint

Categories: 
  Primary: cs.SE
  Cross-list: cs.AI (可选)

License: CC BY 4.0 (推荐，允许他人引用)
```

### 4.3 上传文件

1. 上传 .tex 文件（或 PDF）
2. 上传图片文件（如有）
3. 点击 "Process" 编译
4. 预览 PDF，确认无误

### 4.4 提交

1. 确认所有信息正确
2. 点击 "Submit"
3. 等待处理（通常 1-2 个工作日）

---

## 5. Endorsement（背书）机制

### 5.1 什么是 Endorsement

arXiv 要求首次在某分类提交的作者获得该分类的"背书"，防止垃圾论文。

### 5.2 如何获得 Endorsement

**方法1：自动获得**
- 使用 .edu 邮箱注册
- 某些机构自动获得背书权

**方法2：请求背书**
- 找一个已在 cs.SE 发过论文的人
- 请他们在 arXiv 上为你背书
- 他们会收到邮件，点击确认即可

**方法3：联系 arXiv**
- 如果找不到背书人，可联系 arXiv 管理员
- 提供你的学术背景证明

### 5.3 背书请求模板

```
Subject: Request for arXiv Endorsement (cs.SE)

Dear [Name],

I am writing to request your endorsement for submitting 
a paper to arXiv in the cs.SE category.

Paper Title: ODD: Output-Driven Development - A Novel 
Methodology for AI-Assisted Software Engineering

Brief Description: This paper introduces a new software 
development methodology designed for AI-assisted development...

I would greatly appreciate your endorsement.

Best regards,
[Your Name]
```

---

## 6. 提交后流程

### 6.1 时间线

| 阶段 | 时间 |
|------|------|
| 提交 | Day 0 |
| 处理中 | 1-2 工作日 |
| 上线 | 通常下一个工作日 14:00 EST |
| 获得 arXiv ID | 上线时 |

### 6.2 arXiv ID 格式

```
arXiv:2601.12345

2601 = 2026年1月
12345 = 序号
```

### 6.3 引用格式

```bibtex
@article{author2026odd,
  title={ODD: Output-Driven Development},
  author={Your Name},
  journal={arXiv preprint arXiv:2601.XXXXX},
  year={2026}
}
```

---

## 7. 后续操作

### 7.1 更新论文

- 可以提交新版本（v2, v3...）
- 所有版本都会保留
- 建议：重大修改才更新

### 7.2 建立优先权

arXiv 提交时间戳是**法律认可的优先权证据**：
- 记录你的提交时间
- 保存确认邮件
- 截图 arXiv 页面

### 7.3 后续发表

arXiv 预印本不影响正式发表：
- 可以同时投稿期刊/会议
- 大多数期刊接受 arXiv 预印本
- 正式发表后可在 arXiv 添加 DOI 链接

---

## 8. 常见问题

**Q: arXiv 是否算正式发表？**
A: 不算。arXiv 是预印本服务器，但学术界广泛认可，可建立优先权。

**Q: 会被拒绝吗？**
A: 很少。只要格式正确、内容是学术性的，基本都会通过。

**Q: 可以撤回吗？**
A: 不能删除，但可以标记为"withdrawn"。

**Q: 需要付费吗？**
A: 完全免费。

---

## 9. 快速行动清单

```
□ 1. 注册 arXiv 账号
□ 2. 将论文转换为 LaTeX/PDF
□ 3. 获取 endorsement（如需要）
□ 4. 提交论文
□ 5. 等待上线（1-2天）
□ 6. 获得 arXiv ID，建立优先权
□ 7. 开始投稿正式期刊/会议
```

---

*祝发表顺利！*
