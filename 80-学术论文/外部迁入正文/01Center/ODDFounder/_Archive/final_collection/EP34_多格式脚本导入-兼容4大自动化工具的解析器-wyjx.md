# 多格式脚本导入：兼容4大自动化工具的解析器

> **作者**: Fuyi ( ODDFounder  fuyi.it@live.cn )
> **日期**: 2026-01-11
> **标签**: 编译器, 脚本解析, 兼容性, wyjx, 自动化

---

## 摘要

自动化圈子山头林立：按键精灵（Q语言）、AutoHotkey (AHK)、触动精灵 (Lua)、大漠插件。用户迁移成本极高。**wyjx (无影键侠)** 内置了一个**通用脚本解析器**，能够读取这些竞品的脚本格式，将其转换为 wyjx 的内部中间语言 (IR)，实现了"一键迁移"。

---

## 一、脚本的巴别塔

*   **按键精灵**：`KeyPress 65, 1`
*   **AHK**: `Send, A`
*   **触动**: `touchDown(100, 100)`

虽然语法不同，但核心语义是相通的：点击、按键、找色、延时。

---

## 二、解析器架构

wyjx 采用了一个简化的编译器前端架构。

### 2.1 词法分析 (Lexer)
将源代码拆解为 Token 流。
*   识别关键字：`KeyPress`, `Send`, `Sleep`...
*   识别参数：`65`, `100`, `"hello"`.

### 2.2 语法分析与映射 (Parser & Mapper)
将 Token 流映射到 wyjx 的 **IR (Intermediate Representation)**。

| wyjx IR | 按键精灵 | AHK |
| :--- | :--- | :--- |
| `ACTION_KEY_PRESS` | `KeyPress` | `Send` |
| `ACTION_DELAY` | `Delay` | `Sleep` |
| `ACTION_FIND_PIC` | `FindPic` | `ImageSearch` |

### 2.3 坐标系转换
这是最坑的地方。
*   有的工具是相对于**屏幕左上角**。
*   有的工具是相对于**窗口客户区**。
解析器在导入时，会根据脚本头部的声明（如 `SetSimMode`），自动添加坐标转换修饰符。

---

## 三、UtilsTaskImportExport.pas 实现

在 wyjx 的代码中，`ImportTask` 函数不仅支持 JSON，还支持文本解析。

```pascal
if IsMQScript(Content) then
  Task := ParseMQ(Content)
else if IsAHKScript(Content) then
  Task := ParseAHK(Content);
```

对于不支持的高级语法（如复杂的 `If...Else` 嵌套），wyjx 会将其保留为**注释**，或者转换为 wyjx 的 `ConditionBlock`，尽最大努力保持逻辑完整。

---

## 四、总结

兼容性是后来者的通行证。
通过内置多格式解析器，wyjx 降低了用户的迁移门槛，让用户可以复用沉淀多年的脚本资产。这是技术实力对商业竞争的直接降维打击。

---

*下一篇预告：《053-配置执行分离：自动化平台的双端架构》*
