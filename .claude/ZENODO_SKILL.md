# Zenodo Manager Skill

> 用途：管理一元论理论体系的 Zenodo 发布、数据查询、记录修复。
> 触发：用户提到 Zenodo、DOI、发布、上传、论文预印本时自动加载。

---

## 账号信息

| 字段 | 值 |
|------|-----|
| **API Token** | `8wHeH4SWs3OlljaNzbnrpDCfkHPcpIih7NrjU2FBTFXrP7xs6Tteku2HjkpZ` |
| **ORCID** | `0009-0008-1251-2632` |
| **Owner ID** | `1511969` |
| **作者名（API）** | `Yi Fu` |
| **作者全名** | Yi Fu（付毅，ODDFounder，fuyi.it@live.cn） |
| **Token Header** | `Authorization: Bearer {token}` |

---

## 核心记录（11 条）

### 公开法源链
| 层 | DOI | Zenodo ID | 日期 |
|-----|-----|-----------|------|
| DM | `10.5281/zenodo.19852505` | 19852505 | 2026-04-28 |
| ASTO | `10.5281/zenodo.19856467` | 19856467 | 2026-04-28 |
| ECET | `10.5281/zenodo.19855877` | 19855877 | 2026-04-28 |
| TAT | `10.5281/zenodo.19855204` | 19855204 | 2026-04-28 |
| ODD v1.0 | `10.5281/zenodo.18207648` | 18207648 | 2026-01-10 |
| ODD v2.0 CN | `10.5281/zenodo.19856890` | 19856890 | 2026-04-28 |

### 诊断/承接/显影
| 层 | DOI | Zenodo ID |
|-----|-----|-----------|
| COP | `10.5281/zenodo.19856272` | 19856272 |
| RT6 | `10.5281/zenodo.19856379` | 19856379 |
| LMM | `10.5281/zenodo.19856528` | 19856528 |

### 旧记录修复/去重
| 项 | DOI | Zenodo ID |
|-----|-----|-----------|
| ASTO01 修复 | `10.5281/zenodo.19857091` | 19857091 |
| ASTO02 修复 | `10.5281/zenodo.19857093` | 19857093 |
| ASTO03 修复 | `10.5281/zenodo.19857100` | 19857100 |
| Arbitration 统一 | `10.5281/zenodo.19857145` | 19857145 |

---

## API 工作流

### 1. 查询所有记录
```bash
curl -sL "https://zenodo.org/api/records?q=owners:1511969&sort=mostrecent&size=50"
```

### 2. 查看单条记录详情 + 统计
```bash
curl -sL "https://zenodo.org/api/records/{record_id}"
# stats: downloads, unique_downloads, views, unique_views
```

### 3. 创建沉积 → 上传 → 发布（完整流程）

```python
import json, urllib.request
T = 'Bearer 8wHeH4SWs3OlljaNzbnrpDCfkHPcpIih7NrjU2FBTFXrP7xs6Tteku2HjkpZ'

def publish_zenodo(pdf_path, filename, title, desc, keywords, version='v1.0', related_dois=None):
    # 1. Create deposition
    req = urllib.request.Request('https://zenodo.org/api/deposit/depositions', data=b'{}',
        headers={'Authorization': T, 'Content-Type': 'application/json'}, method='POST')
    dep = json.loads(urllib.request.urlopen(req).read())
    did = dep['id']
    
    # 2. Upload PDF
    boundary = '---BOUNDARY'
    body = b''
    with open(pdf_path, 'rb') as f: fd = f.read()
    body += f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: application/pdf\r\n\r\n'.encode() + fd + f'\r\n--{boundary}--\r\n'.encode()
    urllib.request.urlopen(urllib.request.Request(
        f'https://zenodo.org/api/deposit/depositions/{did}/files', data=body,
        headers={'Authorization': T, 'Content-Type': f'multipart/form-data; boundary={boundary}'}, method='POST'))
    
    # 3. Set metadata
    meta = {'metadata': {
        'title': title, 'creators': [{'name': 'Yi Fu', 'orcid': '0009-0008-1251-2632'}],
        'description': desc, 'keywords': keywords, 'publication_date': '2026-04-28',
        'version': version, 'language': 'zho',
        'upload_type': 'publication', 'publication_type': 'preprint',
        'license': 'cc-by-4.0', 'access_right': 'open'
    }}
    if related_dois:
        meta['metadata']['related_identifiers'] = related_dois
    urllib.request.urlopen(urllib.request.Request(
        f'https://zenodo.org/api/deposit/depositions/{did}',
        data=json.dumps(meta).encode('utf-8'),
        headers={'Authorization': T, 'Content-Type': 'application/json'}, method='PUT'))
    
    # 4. Publish
    result = json.loads(urllib.request.urlopen(urllib.request.Request(
        f'https://zenodo.org/api/deposit/depositions/{did}/actions/publish',
        headers={'Authorization': T}, method='POST')).read())
    return result['doi'], did
```

### 4. 创建元数据修复记录（无 PDF，仅 README.txt）

```python
def publish_metadata_fix(title, desc, keywords, related_dois):
    # 同上流程，但上传一个 README.txt 占位文件
    # 用于 ASTO 修复、Arbitration 去重等场景
```

### 5. 查看某条记录的下载/浏览统计

```python
req = urllib.request.Request(f'https://zenodo.org/api/records/{record_id}')
result = json.loads(urllib.request.urlopen(req).read())
stats = result['stats']
print(f"Downloads: {stats['downloads']}, Views: {stats['views']}")
```

---

## PDF 生成规范

### Markdown → PDF（中文）
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont=SimSun \
  -V monofont=SimHei \
  -V geometry:margin=2.5cm \
  -V fontsize=11pt \
  --toc --toc-depth=2
```

### 中文 PDF 字体要求
- 正文：SimSun（宋体）
- 等宽/强调：SimHei（黑体）
- 引擎：xelatex（必须，lualatex 备选）
- 已知限制：emoji（✅⏳）、Unicode 下标（₀）等特殊字符可能缺失，非关键

### 合并多文件
```python
# 写 header → 逐个 append 源文件内容 → \newpage 分隔
# 输出合并 .md → pandoc 转 PDF
```

---

## 文件命名规范

### Zenodo 文件名（ASCII only）
```
{LAYER}_{English_Name}_v{version}.pdf
例：DM_Difference_Monism_Unified_Review_v1.1.pdf
例：TAT_Accountability_Threshold_v1.0.pdf
```

### 本地源文件
```
{层号}-{中文名}/{文件名}.md
例：10-哲学核心层（DM）/DM.P00.存在论地基.md
```

---

## 已发布的理论包结构

每个 Zenodo 记录 = 1 个 PDF，内部结构：
1. 统一母文件 / 总览
2. 核心理论/公理/协议
3. 案例卡/走通示例
4. 桥接/接口文档

---

## 本地项目路径

| 用途 | 路径 |
|------|------|
| 项目根 | `D:/_Progs/一元论/` |
| DM 送审包 | `00-索引与导航/DM.统一送审包.v1.1.md` |
| ASTO papers | `20-应用框架层（ASTO）/papers/` |
| ECET | `30-文明演化层（ECET）/` |
| TAT | `40-责任架构层（TAT）/` |
| ODD docs | `50-工程方法层（ODD）/ODD-main/docs/` |
| COP | `51-认知计算层（COP）/` |
| LMM public | `52-认知方法层（LMM）/public/` |
| RT6 | `53-操作方法层（RT6）/` |
| better.md | 根目录（任务追踪） |
