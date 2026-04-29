# Junction链接迁移：让C盘瘦身程序无感知

> **作者**: Fuyi ( ODDFounder  fuyi.it@live.cn )
> **日期**: 2026-01-11
> **标签**: Windows API, NTFS, Junction, 目录迁移, MoveC, Delphi

---

## 摘要

C盘空间不足是Windows用户的永恒痛点。直接剪切粘贴文件夹（如 `Users` 或 `Program Files`）会导致系统崩溃或程序报错。**MoveC** 利用 NTFS 文件系统的 **Junction (目录联接)** 特性，实现了一种"偷梁换柱"的迁移方案：将文件物理移动到 D 盘，但在 C 盘原位置留下一个"传送门"。程序对此完全无感知。本文解析这一黑科技的底层实现。

---

## 一、什么是 Junction？

在 NTFS 文件系统中，Junction Point（联接点）是一种特殊的重解析点（Reparse Point）。
*   它类似于 Linux 的软链接（Symlink），但专门用于**目录**。
*   它对应用程序是**透明**的。
    *   程序访问 `C:\Data`。
    *   文件系统自动重定向到 `D:\Data`。
    *   程序以为自己还在 C 盘读写。

这就是 MoveC 的核心原理：**物理迁移，逻辑保留。**

---

## 二、迁移流程设计

在 `uDirectoryMigration.pas` 和 `uFileOperations.pas` 中，我们实现了严谨的迁移事务：

### 2.1 第一步：安全检查 (Pre-Check)
*   **占用检查**：检查源目录下的文件是否被占用（File in use）。如果被占用，提示用户关闭相关程序。
*   **空间检查**：确保目标磁盘（D盘）有足够空间。
*   **权限检查**：确保有管理员权限。

### 2.2 第二步：数据复制 (Copy)
使用 `Robocopy` 或 Delphi 的 `TDirectory.Copy` 将数据完整复制到目标位置。
*   **关键点**：必须保留文件的**时间戳**、**属性**（只读/隐藏）和**ACL权限**。否则迁移后程序可能因权限不足报错。

### 2.3 第三步：原子切换 (Switch)
这是最危险的一步。
1.  **重命名**：将源目录 `C:\Data` 重命名为 `C:\Data.bak`。（不要直接删除，留后路！）
2.  **创建 Junction**：在 `C:\Data` 创建一个指向 `D:\Data` 的 Junction。
    *   API: `CreateSymbolicLink` (带 `SYMBOLIC_LINK_FLAG_DIRECTORY` 标志) 或 `DeviceIoControl` 设置 Reparse Point。

### 2.4 第四步：验证与清理 (Verify & Cleanup)
1.  **验证联通性**：尝试通过 `C:\Data\test.txt` 读取文件，确认能读到 `D:\Data\test.txt`。
2.  **删除备份**：如果验证成功，删除 `C:\Data.bak` 释放空间。（MoveC 通常保留备份让用户手动删，以防万一）。

---

## 三、技术挑战与坑

### 3.1 循环链接 (Infinite Loop)
在扫描目录时，必须识别 Junction，否则递归扫描会陷入死循环。
*   *解决*：检查 `FileAttributes` 是否包含 `FILE_ATTRIBUTE_REPARSE_POINT`。

### 3.2 权限继承 (ACL)
简单的 `CopyFile` 不会复制 ACL。
*   *解决*：使用 `Robocopy /COPYALL /E` 参数，或使用 Windows API `GetNamedSecurityInfo` / `SetNamedSecurityInfo` 复制 SD (Security Descriptor)。

### 3.3 系统目录保护
某些目录（如 `Windows`, `Program Files`）受到 TrustedInstaller 保护，普通管理员无法移动。
*   *MoveC 策略*：**避开系统核心目录**。主要针对 `Users\Documents`, `AppData\Local\Temp`, `Docker Images`, `Gradle Cache` 等用户数据和开发工具缓存。这些是"大户"且迁移风险低。

---

## 四、代码片段 (Delphi)

```pascal
function CreateJunction(const LinkPath, TargetPath: string): Boolean;
begin
  // 必须确保 TargetPath 存在且是绝对路径
  if not TDirectory.Exists(TargetPath) then Exit(False);
  
  // 调用 Kernel32.dll
  Result := CreateSymbolicLink(PChar(LinkPath), PChar(TargetPath), 
    SYMBOLIC_LINK_FLAG_DIRECTORY or SYMBOLIC_LINK_FLAG_ALLOW_UNPRIVILEGED_CREATE);
    
  if not Result then
    RaiseLastOSError; // 记录错误日志
end;
```

---

## 五、总结

Junction 迁移技术是 MoveC 的灵魂。它完美地平衡了**空间释放**和**兼容性**。
通过这套机制，用户可以在不重装系统、不重装软件的情况下，瞬间为 C 盘腾出几十 GB 空间。这是对 Windows 底层机制的一种优雅利用。

---

*下一篇预告：《074-两级扫描缓存：让磁盘分析快10倍》*
