# ODD 论文投稿指南

## 一、论文基本信息

**标题**: Output-Driven Development (ODD): Foundations of Artifact Legitimacy in AI-Native Software Engineering

**作者**: Yi Fu (ODDFounder)

**当前格式**: IEEEtran (会议格式)

---

## 二、推荐期刊对比

### 首选：IEEE Software

| 项目 | 要求 | 当前论文状态 |
|------|------|-------------|
| **网站** | https://www.computer.org/csdl/magazine/so/write-for-us/14426 | - |
| **投稿系统** | https://ieee.atyponrex.com/journal/sw-cs | - |
| **字数限制** | 4,200 词（含图表，每图/表算 250 词） | ⚠️ 当前约 6,000+ 词，需精简 |
| **摘要** | ≤150 词 | ⚠️ 当前约 180 词，需精简 |
| **参考文献** | ≤15 篇（不计入字数） | ✅ 当前 16 篇，基本符合 |
| **特殊要求** | 需提供 3 条 practitioner insights | ⚠️ 需添加 |
| **作者照片** | 必须提供 | ⚠️ 需准备 |
| **审稿周期** | 约 3-6 个月 | - |
| **影响因子** | ~2.5 | - |

### 备选：Journal of Systems and Software (JSS)

| 项目 | 要求 | 当前论文状态 |
|------|------|-------------|
| **网站** | https://www.sciencedirect.com/journal/journal-of-systems-and-software | - |
| **投稿系统** | Elsevier Editorial Manager | - |
| **字数限制** | 无硬性限制（建议 8,000-12,000 词） | ✅ 符合 |
| **摘要** | 无硬性限制 | ✅ 符合 |
| **参考文献** | 无限制 | ✅ 符合 |
| **特殊要求** | 鼓励 Open Science（数据/代码共享） | ⚠️ 可补充 Zenodo 链接 |
| **审稿周期** | 约 4-8 个月 | - |
| **影响因子** | 4.1 | - |
| **CiteScore** | 9.4 | - |

---

## 三、IEEE Software 投稿版本修改建议

### 3.1 摘要修改（≤150 词）

**当前摘要** (约 180 词)：过长，需精简

**建议修改版**：

```
Large Language Models shift software engineering's bottleneck from producing code to governing outcomes. Traditional responsibility anchors—authorship and code review—no longer scale when AI generates changes faster than humans can review. We introduce Output-Driven Development (ODD), a governance paradigm treating artifacts (verifiable outputs with use-value) as the unit of control, acceptance contracts as legitimacy boundaries, and reallocating responsibility from authorship to arbitration. Under ODD, humans approve contracts and accept/reject artifacts at explicit decision points; the system generates evidence (tests, adversarial probes, mutation testing) and seals accepted artifacts with auditable records. We provide operational definitions of artifact legitimacy, a vignette showing high-risk integration shipping without routine code review, and discuss implications for verification economics and organizational accountability.
```
(约 120 词)

### 3.2 关键词

**当前关键词**：
```
Output-Driven Development, AI-Native Software Engineering, Software Governance, 
Artifact Legitimacy, Acceptance Contracts, Mutation Testing, Provenance, Accountability
```

**IEEE Software 建议关键词**（更贴近实践者）：
```
AI-assisted development, software governance, artifact verification, 
acceptance contracts, mutation testing, software accountability
```

### 3.3 必须添加：3 条 Practitioner Insights

在摘要后添加：

```latex
\textbf{Practitioner Insights:}
\begin{itemize}
\item \textbf{Shift control from code review to artifact acceptance}: Define explicit contracts before AI generates code; accept artifacts based on evidence, not line-by-line inspection.
\item \textbf{Use layered verification as your quality gate}: Combine unit tests, adversarial probes, and mutation testing to build defensible acceptance records.
\item \textbf{Seal accepted artifacts with auditable records}: Bind contract, code, tests, and environment via hashes to preserve accountability when implementations are regenerated.
\end{itemize}
```

### 3.4 字数精简建议

当前论文约 6,000+ 词，需精简至 4,200 词以内：

| 章节 | 当前状态 | 建议 |
|------|----------|------|
| Introduction | 过长 | 合并 I-A 到 I-E，删除重复论述 |
| Core concepts | 适中 | 保留 |
| ODD in context | 适中 | 精简 Table I |
| Implications | 过长 | 合并相似小节 |
| Limitations | 过长 | 精简为 1-2 段 |
| Conclusion | 适中 | 保留 |

---

## 四、JSS 投稿版本（备选）

如果选择 JSS，当前论文基本符合要求，只需：

1. **格式转换**：从 IEEEtran 转为 Elsevier 模板
2. **添加 Open Science 声明**：
   ```
   Data Availability: The ODD framework specification is available at 
   https://doi.org/10.5281/zenodo.18207648
   ```
3. **强化实证部分**：JSS 偏好有实证支撑的论文，可在 Future Work 中明确实证计划

---

## 五、投稿流程

### IEEE Software 投稿步骤

1. **预投稿咨询**（可选但推荐）
   - 发送摘要至主编：sigrid.eldh@ieee.org
   - 确认主题适合性

2. **准备材料**
   - [ ] 精简后的论文 PDF
   - [ ] 作者照片（高清）
   - [ ] 3 条 Practitioner Insights
   - [ ] Cover Letter

3. **提交**
   - 访问：https://ieee.atyponrex.com/journal/sw-cs
   - 选择 "Submit Manuscript"
   - 上传所有材料

4. **Cover Letter 模板**

```
Dear Editor-in-Chief,

We submit our manuscript "Output-Driven Development (ODD): Foundations of 
Artifact Legitimacy in AI-Native Software Engineering" for consideration 
in IEEE Software.

This paper addresses a timely challenge: as AI-assisted code generation 
becomes mainstream, traditional quality gates (code review, authorship 
tracking) no longer scale. We propose ODD, a governance paradigm that 
shifts control from code inspection to artifact acceptance under explicit 
contracts.

Key contributions:
1. Reframes software governance for AI-native development
2. Introduces artifact legitimacy as the unit of control
3. Provides operational definitions and a practical vignette

We believe this work aligns with IEEE Software's mission to bridge 
research and practice, offering actionable insights for practitioners 
navigating AI-assisted development.

Sincerely,
Yi Fu
```

---

## 六、论文内容检查结果

### ✅ 符合要求

| 项目 | 状态 |
|------|------|
| 原创性 | ✅ 提出新范式 ODD |
| 实践导向 | ✅ 有具体 vignette 和 checklist |
| 参考文献质量 | ✅ 引用 ICSE、USENIX Security 等顶会 |
| 结构完整 | ✅ Introduction → Core → Context → Implications → Limitations → Conclusion |
| 图表 | ✅ 有 Figure 1 和 Table I |

### ⚠️ 需要修改

| 项目 | 问题 | 建议 |
|------|------|------|
| 字数 | 超出 IEEE Software 限制 | 精简至 4,200 词 |
| 摘要 | 超出 150 词限制 | 精简至 120-150 词 |
| Practitioner Insights | 缺失 | 添加 3 条 |
| 作者照片 | 缺失 | 准备高清照片 |
| 格式 | 当前为会议格式 | 如投 JSS 需转换 |

### ⚠️ 潜在风险

| 风险 | 说明 | 缓解措施 |
|------|------|----------|
| 缺乏实证 | 论文明确声明无实证验证 | 在 Limitations 中诚实说明，强调这是 foundations paper |
| 概念性论文 | IEEE Software 偏好实践案例 | 强化 vignette 部分，添加更多实践细节 |

---

## 七、时间规划建议

| 阶段 | 任务 | 建议时间 |
|------|------|----------|
| Week 1 | 精简论文至 4,200 词 | 3-5 天 |
| Week 1 | 修改摘要、添加 Insights | 1 天 |
| Week 2 | 准备作者照片、Cover Letter | 1-2 天 |
| Week 2 | 预投稿咨询（可选） | 等待回复 |
| Week 3 | 正式提交 | 1 天 |
| Week 3-12 | 等待审稿 | 约 3-6 个月 |

---

## 八、联系方式

- **IEEE Software 主编**: sigrid.eldh@ieee.org
- **IEEE Software 投稿系统**: https://ieee.atyponrex.com/journal/sw-cs
- **JSS 投稿系统**: https://www.editorialmanager.com/jss/

---

*指南生成时间: 2026-01-28*
