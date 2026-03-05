CH23 = r'D:\_Progs\01Center\ASTO\小说故事\《凛冬之宪》\2.0\第23章_峰会前夕-产出物.md'

with open(CH23, 'r', encoding='utf-8-sig') as f:
    text = f.read()

old_section = '''## [B 补丁]《紧急修补 Diff（热修补丁，凌晨上线｜为了救命写丑点）》

> 文件编号：PATCH-DIFF-2055-01
> 物理状态：代码审查界面的截图。代码风格极其丑陋，充满了临时的硬编码。

**【Commit Message】**
`Hotfix: 紧急熔断"恶意合规"攻击。这不是优雅的代码，但它能救命。`

**【代码片段】**
```diff
+ // 丑陋的补丁 #20550214 by ShenZX
+ // 如果检测到单一来源的"完美合规"举报流超过阈值
+ // 不要相信它。哪怕它是对的。
+ if (report_stream.is_perfectly_compliant() && report_rate > HUMAN_LIMIT) {
+     // 触发"人工降速"
+     system.response_time = "INFINITE"; // 违反时效性法案？去他的法案。
+     alert("Human intervention needed. Logic implies malice.");
+     return; 
+ }
```

**【Reviewer Note】**
`LGTM (Looks Good To Me). But it's ugly as hell. —— XuD`
`Live with it. —— JiK`'''

new_section = '''## [B 补丁]《紧急修补 Diff（热修补丁，凌晨上线｜为了救命写丑点）》

> 文件编号：PATCH-DIFF-2055-01
> 物理状态：紧急打印的条款修订单，红笔批改痕迹密布。右下角沈知行签字，墨迹未干。

**【修订说明】**
紧急熔断"恶意合规"攻击路径。这不是优雅的制度，但它能救命。

**【条款变更（Diff）】**

--- 原文：《算法响应法》第 7.3 条
+++ 热修补丁（临时覆盖，24h 日落）

－ 系统须在 15 分钟内处理每一条举报，否则视为违规。
＋ 当单一来源的"完全合规"举报流超过人类正常频率阈值时，系统须暂停自动处理，强制转入人工审核通道。
＋ 在人工审核完成前，不得触发任何账户冻结。
＋ 时效性条款在人工审核期间自动挂起（不视为违规）。

【沈知行手写批注】"哪怕它合规，也不要相信它。完美本身就是最大的可疑。"
【许冬批注】"丑，但能用。"
【姬可批注】"先活着再说。"'''

text_normalized = text.replace('\r\n', '\n')
old_normalized = old_section.replace('\r\n', '\n')

if old_normalized in text_normalized:
    text_normalized = text_normalized.replace(old_normalized, new_section, 1)
    with open(CH23, 'w', encoding='utf-8') as f:
        f.write(text_normalized)
    print('OK: Replaced code-style diff with policy-style diff')
else:
    print('MISS: old section not found')
