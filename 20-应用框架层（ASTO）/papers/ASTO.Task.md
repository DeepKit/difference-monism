# ASTO 核心哲学文档发表对齐计划 (Alignment Task)

> **目标**：确保 ASTO 哲学核心 (P01-P13 + U01-U03) 文档在术语、格式与结构上完全对齐，达到可发表标准。
> **基准**：以 `ASTO.P03.认识论.Phil.md` 的内容和 `ASTO.U02.Glossary.zh-en.v1.0.md` 的定义为最高准则。

## 1. 基础设施与标准 (Infrastructure)

- [x] **术语表更新 (U02 Refinement)**
    - [x] 基于 P03 增补认识论核心术语 (Epistemology, Knowing, Meta-Constraints)。
    - [x] 确认无 Peircean Firstness 等旧术语残留。
- [x] **元数据标准制定 (Metadata Standard)**
    - [x] 制定统一的 YAML Front Matter 模板。
    - [x] 确定 P 系列所有文档的版本号策略。

## 2. 核心文档对齐 (Core Documents Alignment)

### P01. 非此 (Not-This)
- [x] **术语扫描**：检查是否存在旧版 "Firstness/Secondness" 或物理化 "Force/Field" 描述。
- [x] **头部注入**：添加标准 YAML Metadata。
- [x] **结构检查**：确保目录 (TOC) 存在且层级正确。

### P02. 序章 (Prologue)
- [x] **术语扫描**：同上。
- [x] **头部注入**：同上。

### P03. 认识论 (Epistemology)
- [x] **基准确立**：已作为术语基准。
- [x] **完整性检查**：确认后半部分（工程附录等）是否需要与正文剥离或保留。
- [x] **头部注入**：更新 YAML Metadata。

### P04. 宣言 (Manifesto)
- [x] **术语扫描**：重点检查宣言中激进的口号是否符合新定义。
- [x] **版本确认**：确认 v12.5 是否为最终发布版本号。
- [x] **头部注入**：同上。

### P05. 公理 (Axioms)
- [x] **元约束对齐**：确认“行动三问/元约束”的表述与 P03 完全一致。
- [x] **术语扫描**：同上。
- [x] **头部注入**：同上。

### P06 - P13 (Values, Freedom, Critique, etc.)
- [x] **批量术语扫描**：对剩余文件进行关键词 `Firstness`, `Secondness`, `Thirdness` 的批量 Grep 检查。
- [x] **引用一致性**：检查对 P01/P03/P05 的引用是否指向正确版本。
- [x] **头部注入**：批量添加 Metadata。
- [x] **可读性与表达力优化 (Expressiveness)**：
    - [x] **P09 (批判)**：根据专家建议优化论证结构与表达。
    - [x] **P11 (韧性)**：增强理论韧性与自我免疫的阐述。
    - [x] **P13 (终章)**：提升文学性与开放式结尾的感染力。

## 3. 辅助文档 (Utility Documents)

### U01. 图序 (Figures)
- [x] **图表核对**：确认图表标题与 U02 术语表一致。

### U03. 可视化集 (Visualizations)
- [x] **Mermaid 代码更新**：如果术语有变更（如 Firstness -> Monistic），需更新 Mermaid 源码中的 Label。

## 4. 最终验证 (Final Verification)

- [x] **构建测试**：尝试将一份核心文档转换为 PDF/HTML，验证排版效果。（P04 → HTML 143KB，Python markdown 构建通过）
- [x] **交叉引用测试**：随机抽取 5 处跨文档引用进行核实。（A01:132/222/223、P03:1202、P04:1481，全部解析正常）

