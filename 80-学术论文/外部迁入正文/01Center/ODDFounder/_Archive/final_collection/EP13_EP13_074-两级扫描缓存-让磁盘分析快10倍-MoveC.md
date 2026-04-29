# 两级扫描缓存：让磁盘分析快10倍

> **作者**: Fuyi ( ODDFounder  fuyi.it@live.cn )
> **日期**: 2026-01-11
> **标签**: 性能优化, 缓存策略, 文件扫描, MoveC, Delphi

---

## 摘要

磁盘分析工具（如 WizTree, SpaceSniffer）的核心体验指标是**速度**。扫描几百万个文件，如果每次都从头读取 MFT 或遍历目录，用户体验会很差。**MoveC** 引入了 **内存 + 磁盘 两级缓存机制**。本文揭秘这套缓存策略如何将二次扫描速度提升 10 倍以上。

---

## 一、慢在哪里？

在 Windows 上遍历目录（`FindFirstFile` / `FindNextFile`）本身是昂贵的 IO 操作。
*   **机械硬盘 (HDD)**：随机读取性能极差，磁头跳来跳去。
*   **固态硬盘 (SSD)**：虽然快，但系统调用的开销依然存在。
*   **文件数量级**：C盘通常有 50万-200万 个文件。单线程遍历需要几十秒甚至几分钟。

---

## 二、两级缓存架构

MoveC 并没有像 WizTree 那样直接解析 NTFS MFT（那样需要驱动级权限且风险较高），而是采用了更通用的 API 遍历，通过缓存来加速。

### 2.1 L1: 内存缓存 (TScanCache)

*   **数据结构**：`TDictionary<string, TFolderInfo>`。
*   **内容**：存储目录的统计信息（大小、文件数、修改时间）。
*   **生命周期**：程序运行期间有效。
*   **作用**：用户在 UI 上点击"返回上一级"或切换视图时，瞬间呈现，无需重扫。

### 2.2 L2: 磁盘缓存 (SQLite/Binary)

*   **数据结构**：序列化的二进制文件或 SQLite 数据库。
*   **内容**：完整的目录树快照。
*   **位置**：`AppData\Local\MoveC\Cache\drive_c.dat`。
*   **作用**：程序关闭后重启，依然能利用上次的扫描结果。

---

## 三、增量更新与脏检查 (Dirty Check)

缓存最大的难题是**一致性**。如果文件变了怎么办？
MoveC 采用了一种**启发式脏检查**策略。

### 3.1 根目录检查
每次启动时，快速检查 C 盘根目录及一级子目录的 `LastWriteTime`。如果一级目录没变，大概率内部大结构没变。

### 3.2 USN Journal (可选)
对于高级模式，MoveC 可以监听 NTFS 的 **USN Journal (Update Sequence Number)**。
*   USN 记录了所有文件的变更。
*   对比上次扫描时的 USN ID，如果变动很小，直接从缓存加载。
*   如果变动很大（如安装了新软件），触发后台重新扫描。

### 3.3 惰性验证 (Lazy Verification)
当用户点击具体某个文件夹（如 `Downloads`）时，MoveC 会发起一个**轻量级验证**：
*   读取该文件夹的当前 `LastWriteTime`。
*   如果与缓存不一致，立即重新扫描该文件夹（Partial Rescan）。
*   更新缓存中的对应节点，并向上冒泡更新父节点的统计信息。

---

## 四、uDiskAnalyzer.pas 的实现细节

在 MoveC 的代码中，`uDiskAnalyzer` 是核心调度器。

```pascal
procedure TDiskAnalyzer.Scan(Path: string);
begin
  // 1. 查缓存
  if FScanCache.TryGetValue(Path, CachedInfo) then
  begin
    if not IsDirty(Path, CachedInfo.Timestamp) then
    begin
      DoProgress('Loaded from cache', 100);
      Exit;
    end;
  end;

  // 2. 缓存失效，执行物理扫描
  RealScan(Path);
  
  // 3. 更新缓存
  FScanCache.AddOrSetValue(Path, NewInfo);
end;
```

---

## 五、效果对比

*   **首次扫描 (Cold Scan)**: 45秒 (C盘, 500GB, 100万文件)。
*   **二次扫描 (Warm Scan)**: **3秒** (从磁盘缓存加载)。
*   **UI 响应**: **< 0.1秒** (从内存缓存读取)。

这 10 倍的提升，让 MoveC 从一个"扫描工具"变成了一个"文件浏览器"。用户感觉不到它在扫描，只觉得它**就在那里**。

---

## 六、总结

性能优化的尽头是**不工作**。
*   缓存让程序"不读取磁盘"。
*   脏检查让程序"不处理未变更的数据"。

MoveC 的两级缓存设计，是用空间换时间（RAM/Disk Space for CPU/IO Time）的经典案例。在桌面应用开发中，**状态持久化**是提升体验的杀手锏。

---

*下一篇预告：《107-双键快启系统：60个程序两步直达的设计》*
