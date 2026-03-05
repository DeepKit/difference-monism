# -*- coding: utf-8 -*-
"""Apply all B-type structural changes to 《凛冬之宪》"""

import os

FILE = os.path.join(os.path.dirname(__file__),
                    'ASTO.凛冬之宪--艰难的前进历程.md')

with open(FILE, 'r', encoding='utf-8') as f:
    text = f.read()

# ============================================================
# B5a: 给妻子叶晗命名 — Ch7 父子对话
# Insert after "他在'不可算法区'下面写下第一条。"
# ============================================================
B5a_anchor = '他在\u201c不可算法区\u201d下面写下第一条。'
B5a_insert = """他在\u201c不可算法区\u201d下面写下第一条。

他写的时候，脑子里闪过叶晗的脸。她在ICU那三个月，他每次签字都是这种感觉——笔尖很重，重得像在替一个不能说话的人做决定。"""
assert text.count(B5a_anchor) == 1, f"B5a anchor not unique: {text.count(B5a_anchor)}"
text = text.replace(B5a_anchor, B5a_insert)
print("B5a done: 叶晗 mentioned in Ch7")

# ============================================================
# B1: Ch14 — 沈知行签全名（真正犯错）
# Replace from "沈知行把笔尖停在'行'的起笔处" to "另一处可能更疼。"
# ============================================================
B1_old_start = '\u6c88\u77e5\u884c\u628a\u7b14\u5c16\u505c\u5728\u201c\u884c\u201d\u7684\u8d77\u7b14\u5904\u3002'  # 沈知行把笔尖停在"行"的起笔处。
B1_old_end = '\u53e6\u4e00\u5904\u53ef\u80fd\u66f4\u75bc\u3002'  # 另一处可能更疼。

idx_start = text.index(B1_old_start)
idx_end = text.index(B1_old_end) + len(B1_old_end)
B1_old = text[idx_start:idx_end]

B1_new = """沈知行把笔尖落在\u201c行\u201d的起笔处。

墨水从笔尖渗出一点，像一滴迟到的血。

他写下去了。

\u201c行\u201d。

三个字合在一起，像一道门槛。跨过去，就回不来。

会议室里安静了一秒。

朱利安的眼睛亮了一下。不是惊喜，是确认。

\u201c但\u2014\u2014\u201d沈知行的声音从喉咙里挤出来。

\u201c冻结必须写到期。必须写责任链。必须公开越权痕迹。必须写明谁被牺牲、怎么补偿。\u201d

他说每一个\u201c必须\u201d时，都在给那个签名加锁。

法务官僚松了一口气，开始在文件上做标注。

朱利安没有反对。他甚至没有还价。

他只是把文件夹翻到附录那一页——那一行\u201c高噪声地区启用加权修平/降权边缘样本\u201d——轻轻推过来。

\u201c这一条，\u201d他说，\u201c技术性的。你的日落条款覆盖。\u201d

沈知行看着那行字。

他的日落条款确实覆盖它。24小时，到期回收。

可\u201c边缘样本\u201d这四个字像一根细小的倒刺，扎进了他的余光里。

他脑子里闪过叶晗——朱利安承诺的试点权限能覆盖到她的医疗数据保护。这很小。小到像一颗灰尘。可灰尘会堵住天平。

他没有划掉那一行。

因为他刚刚签了字。签了字的人，不能一边签一边拆。那会让整份协议像沙子。

朱利安站起来。

\u201c沈工，谢谢。\u201d

他说\u201c谢谢\u201d的语气像说\u201c成交\u201d。

沈知行坐在椅子上没动。

他盯着桌面上那个签名。墨水已经干了。干得很快。

快得像它从一开始就打算变成证据。"""

text = text.replace(B1_old, B1_new)
print("B1a done: Ch14 沈知行 signs full name")

# ============================================================
# B1b: Ch14 产出物 — 修改"半个签名"为"完整签名"
# ============================================================
B1b_old = """## [A \u8840\u8ff9]\u300a\u95ed\u95e8\u4f1a\u8bae\u5907\u5fd8\u5f55\uff08\u534a\u4e2a\u7b7e\u540d + \u5212\u6389\u91cd\u5199\uff5c\u7eb8\u4e0a\u6709\u6c57\u6e0d\uff09\u300b

> \u6587\u4ef6\u7f16\u53f7\uff1aFIN-CLOSED-MEMO-2048-07-001

- \u4f1a\u8bae\u6027\u8d28\uff1a\u95ed\u95e8\uff08\u540e\u7ecf\u7a0b\u5e8f\u6027\u66dd\u5149\uff0c\u516c\u5f00\u8131\u654f\u7248\uff09
- \u5173\u952e\u8bb0\u5f55\uff08\u8131\u654f\u8282\u9009\uff09\uff1a
  - \u201c\u5efa\u8bae\u5728\u9ad8\u566a\u58f0\u5730\u533a\u542f\u7528\u52a0\u6743\u4fee\u5e73/\u964d\u6743\u8fb9\u7f18\u6837\u672c\uff0c\u4ee5\u63d0\u5347\u5168\u56fd\u7a33\u5b9a\u6027\u3002\u201d
  - \u201c\u51bb\u7ed3\u8d4e\u56de/\u63d0\u73b0\uff1a\u5fc5\u987b\u9644\u65e5\u843d\u6761\u6b3e\u4e0e\u8d23\u4efb\u94fe\u3002\u201d
- \u7269\u7406\u75d5\u8ff9\u8bf4\u660e\uff1a\u7b7e\u540d\u5904\u5199\u5230\u201c\u6c88\u77e5\u2026\u201d\u5373\u505c\u6b62\uff1b\u540e\u88ab\u6574\u6bb5\u5212\u6389\u91cd\u5199\uff1b\u7eb8\u53f3\u4e0b\u89d2\u6709\u660e\u663e\u6c57\u6e0d\u62d6\u75d5\u3002"""

B1b_new = """## [A \u8840\u8ff9]\u300a\u95ed\u95e8\u4f1a\u8bae\u5907\u5fd8\u5f55\uff08\u5b8c\u6574\u7b7e\u540d\uff5c\u7eb8\u4e0a\u6709\u6c57\u6e0d\uff09\u300b

> \u6587\u4ef6\u7f16\u53f7\uff1aFIN-CLOSED-MEMO-2048-07-001

- \u4f1a\u8bae\u6027\u8d28\uff1a\u95ed\u95e8\uff08\u540e\u7ecf\u7a0b\u5e8f\u6027\u66dd\u5149\uff0c\u516c\u5f00\u8131\u654f\u7248\uff09
- \u5173\u952e\u8bb0\u5f55\uff08\u8131\u654f\u8282\u9009\uff09\uff1a
  - \u201c\u5efa\u8bae\u5728\u9ad8\u566a\u58f0\u5730\u533a\u542f\u7528\u52a0\u6743\u4fee\u5e73/\u964d\u6743\u8fb9\u7f18\u6837\u672c\uff0c\u4ee5\u63d0\u5347\u5168\u56fd\u7a33\u5b9a\u6027\u3002\u201d
  - \u201c\u51bb\u7ed3\u8d4e\u56de/\u63d0\u73b0\uff1a\u5fc5\u987b\u9644\u65e5\u843d\u6761\u6b3e\u4e0e\u8d23\u4efb\u94fe\u3002\u201d
- \u7269\u7406\u75d5\u8ff9\u8bf4\u660e\uff1a\u7b7e\u540d\u5904\u5b8c\u6574\u5199\u4e0b\u201c\u6c88\u77e5\u884c\u201d\u4e09\u5b57\uff1b\u201c\u884c\u201d\u5b57\u672b\u7b14\u58a8\u6c34\u5fae\u6655\uff1b\u7eb8\u53f3\u4e0b\u89d2\u6709\u660e\u663e\u6c57\u6e0d\u62d6\u75d5\u3002\u9644\u5f55\u201c\u52a0\u6743\u4fee\u5e73\u201d\u6761\u6b3e\u672a\u88ab\u5212\u6389\u3002"""

assert text.count(B1b_old) == 1, f"B1b anchor not unique"
text = text.replace(B1b_old, B1b_new)
print("B1b done: Ch14 产出物 updated")

# ============================================================
# B1c: Ch15 — 牺牲清单中发现自己签字的后果
# Insert after "干净得像历史只会记住胜利者，而把这些人变成了注脚。"
# ============================================================
B1c_anchor = '\u5e72\u51c0\u5f97\u50cf\u5386\u53f2\u53ea\u4f1a\u8bb0\u4f4f\u80dc\u5229\u8005\uff0c\u800c\u628a\u8fd9\u4e9b\u4eba\u53d8\u6210\u4e86\u6ce8\u811a\u3002'
B1c_insert = """干净得像历史只会记住胜利者，而把这些人变成了注脚。

他翻到第七页时停住了。

一个名字旁边的备注栏写着：\u201c补偿延迟（原因：加权修平期间被降权，申诉通道冻结72h）\u201d。

关联文件编号：FIN-CLOSED-MEMO-2048-07-001。

就是他签的那份。

沈知行的指尖按在那行字上，指腹发白。

他曾以为日落条款能兜住一切。24小时，到期回收。

可那72小时的申诉冻结，恰好卡在日落之前。

有人在那72小时里，等不到补偿，也喊不出声。

这不是\u201c差点\u201d。

这是\u201c已经\u201d。"""
assert text.count(B1c_anchor) == 1, f"B1c anchor not unique"
text = text.replace(B1c_anchor, B1c_insert)
print("B1c done: Ch15 牺牲清单关联签字后果")

# ============================================================
# B1d: Ch22 — 加一条UNF条目（加权修平案）
# Insert after "是人性深处那个无论怎么计算都无法被归约的余数。"
# ============================================================
B1d_anchor = '\u662f\u4eba\u6027\u6df1\u5904\u90a3\u4e2a\u65e0\u8bba\u600e\u4e48\u8ba1\u7b97\u90fd\u65e0\u6cd5\u88ab\u5f52\u7ea6\u7684\u4f59\u6570\u3002'
B1d_insert = """是人性深处那个无论怎么计算都无法被归约的余数。

他翻到下一页。空白。

他写：

\u201cUNF-2054-002：加权修平签字案。\u201d

他停了一下。这一条比上一条更疼。因为上一条他可以说\u201c制度的局限\u201d。这一条没有借口。

\u201c通过了哪些护栏？\u201d
他写：*日落条款（24h）。责任链签署。越权痕迹公开。*

\u201c不可逆代价？\u201d
他写：*被降权者在72h申诉冻结期内无法获得补偿。至少一人因此陷入困境。*

\u201c为什么暂不修复？\u201d
他写了三个字，写得很慢，每一笔都像在刻自己的脸：
\u201c我签的。\u201d"""
assert text.count(B1d_anchor) == 1, f"B1d anchor not unique"
text = text.replace(B1d_anchor, B1d_insert)
print("B1d done: Ch22 added UNF-002 entry")

# ============================================================
# B2: Ch21 朱利安加戏
# Insert after K主任说完 "牺牲边缘，是最优解。" and the narrator echo
# Anchor: "如果是以前的沈知行，会同意。因为数学上这是对的。"
# ============================================================
B2_anchor = '\u5982\u679c\u662f\u4ee5\u524d\u7684\u6c88\u77e5\u884c\uff0c\u4f1a\u540c\u610f\u3002\u56e0\u4e3a\u6570\u5b66\u4e0a\u8fd9\u662f\u5bf9\u7684\u3002'
B2_insert = """大屏幕忽然闪了一下。

朱利安的全息投影出现在会场侧面。他不在现场——他从来不在需要流血的现场。背景是一间极简的白色办公室，窗外是另一座城市的天际线。

\u201c沈工，\u201d朱利安说，声音很清晰，像提前录好的，\u201c你们用禁元否决了效率。我尊重。\u201d

他停了一下，像在等掌声。没有掌声。

\u201c但否决不了物理。\u201d他继续说，\u201c那两千个维护工的退休金、医疗、再就业——谁出？\u201d

他摊开手。

\u201c我出。\u201d

会场里有人动了一下。

\u201c但我要数据。\u201d朱利安说，\u201c不是隐私，是脱敏后的职业技能图谱。用来匹配新岗位。你们的慢轨走三年，我的数据能把再就业周期压到八个月。\u201d

他的提议干净、具体、甚至慷慨。

干净得让人挑不出毛病。

沈知行看着那张全息面孔。他想说\u201c不\u201d。

但他嘴里说出来的是：\u201c我不确定。\u201d

这是他第一次没有用\u201c不\u201d回答朱利安。

朱利安笑了。那笑容在全息投影里有一点像素化，但足够真实。

\u201c不确定就好。\u201d他说，\u201c确定的人最危险。\u201d

投影消失了。会场的灯重新亮起来。

如果是以前的沈知行，会同意。因为数学上这是对的。"""
assert text.count(B2_anchor) == 1, f"B2 anchor not unique"
text = text.replace(B2_anchor, B2_insert)
print("B2 done: Ch21 朱利安 added")

# ============================================================
# B4: 姬可补私人裂缝 — Ch23
# Insert after "她手指很快。快得像在逃。逃离那种'完美系统'的幻觉。"
# ============================================================
B4_anchor = '\u5979\u624b\u6307\u5f88\u5feb\u3002\u5feb\u5f97\u50cf\u5728\u9003\u3002\u9003\u79bb\u90a3\u79cd\u201c\u5b8c\u7f8e\u7cfb\u7edf\u201d\u7684\u5e7b\u89c9\u3002'
B4_insert = """她手指很快。快得像在逃。逃离那种\u201c完美系统\u201d的幻觉。

敲到第三十七行时，她的手停了一下。

不是bug。是记忆。

去年冬天，一个翻译员来找她，说有人在Coffee House发了一段语音，很短，像在求助，又像在告别。翻译员问：要不要触发干预？

姬可当时在调另一个更紧急的模块。她看了一眼时间戳，看了一眼风险评分——0.61，低于阈值。

她说：\u201c走标准流程。\u201d

标准流程意味着排队。排队意味着等。

后来那个人没有等到。

系统没有错。阈值没有错。她也没有\u201c错\u201d。

但她知道，那天她可以多看一眼。可以不说\u201c标准流程\u201d。可以——

她把这个念头按回键盘里，继续敲。"""
assert text.count(B4_anchor) == 1, f"B4 anchor not unique"
text = text.replace(B4_anchor, B4_insert)
print("B4 done: Ch23 姬可 private crack added")

# ============================================================
# B3: Ch25 标记为彩蛋
# ============================================================
# Add separator after Ch24 ending (before Ch25)
# Use line-context-aware replacement for B3
B3_old_title = '\n\n# \u7b2c25\u7ae0\uff1a\u672a\u88ab\u542c\u89c1\u7684\u811a\u6b65\u58f0\n\n\u96a7\u9053\u91cc\u6ca1\u6709\u4fe1\u53f7\u3002'
B3_new_title = '\n\n---\n\n> **\uff08\u6b63\u6587\u5b8c\uff09**\n\n---\n\n\n# \u5f69\u86cb\u7ae0\uff1a\u672a\u88ab\u542c\u89c1\u7684\u811a\u6b65\u58f0\n\n\u96a7\u9053\u91cc\u6ca1\u6709\u4fe1\u53f7\u3002'
assert text.count(B3_old_title) == 1, f"B3 anchor not unique: {text.count(B3_old_title)}"
text = text.replace(B3_old_title, B3_new_title)

# Also update the 产出物 title (use surrounding context)
B3_old_artifact = '\n\n# \u7b2c25\u7ae0\uff1a\u672a\u88ab\u542c\u89c1\u7684\u811a\u6b65\u58f0 \u2014 \u7ae0\u540e\u4ea7\u51fa\u7269\n'
B3_new_artifact = '\n\n# \u5f69\u86cb\u7ae0\uff1a\u672a\u88ab\u542c\u89c1\u7684\u811a\u6b65\u58f0 \u2014 \u7ae0\u540e\u4ea7\u51fa\u7269\n'
assert text.count(B3_old_artifact) == 1, f"B3 artifact anchor not unique: {text.count(B3_old_artifact)}"
text = text.replace(B3_old_artifact, B3_new_artifact)
print("B3 done: Ch25 marked as \u5f69\u86cb")

# ============================================================
# Write back
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(text)

print("\n=== All B changes applied successfully ===")
