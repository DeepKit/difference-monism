#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract 章后产出物 sections from main novel file into standalone appendix files.

Rules:
- Ch1: Keep inline with 样张说明 (sample explanation).
- Ch2-21, 彩蛋(25): Extract to standalone files (overwrite old versions).
- Ch22-24: Keep existing standalone files (they have full pre-C-trim content).
- In main file: replace extracted 产出物 with reference lines.
"""

import re
import os

BASE = r"D:\_Progs\01Center\ASTO\小说故事\《凛冬之宪》\2.0"
MAIN = os.path.join(BASE, "ASTO.凛冬之宪--艰难的前进历程.md")

# Chapter ID → standalone filename
FILEMAP = {
    '第01章': '第01章_冰风暴否决案-产出物.md',
    '第02章': '第02章_沈知行的选择-产出物.md',
    '第03章': '第03章_数字广场的诞生-产出物.md',
    '第04章': '第04章_水的契约-产出物.md',
    '第05章': '第05章_清晰度评估-产出物.md',
    '第06章': '第06章_被遗忘的小镇-产出物.md',
    '第07章': '第07章_父亲的目光-产出物.md',
    '第08章': '第08章_基石落成-产出物.md',
    '第09章': '第09章_数据灵魂-产出物.md',
    '第10章': '第10章_伦理委员会-产出物.md',
    '第11章': '第11章_遗产模块-产出物.md',
    '第12章': '第12章_陈默的路-产出物.md',
    '第13章': '第13章_学习契约-产出物.md',
    '第14章': '第14章_危机的焊接-产出物.md',
    '第15章': '第15章_远航者计划-产出物.md',
    '第16章': '第16章_投票与界面-产出物.md',
    '第17章': '第17章_逆熵智能体-产出物.md',
    '第18章': '第18章_最后一次警告-产出物.md',
    '第19章': '第19章_焦痕-产出物.md',
    '第20章': '第20章_微笑的多数-产出物.md',
    '第21章': '第21章_资源倾斜-产出物.md',
    '第22章': '第22章_未完成清单-产出物.md',
    '第23章': '第23章_峰会前夕-产出物.md',
    '第24章': '第24章_凛冬之宪-产出物.md',
    '彩蛋章': '第25章_未被听见的脚步声-产出物.md',
}

# C-trimmed chapters: keep existing standalone files (they have full content)
C_TRIMMED = {'第22章', '第23章', '第24章'}

# Chapters that already have "> 章后产出物见：" reference lines
HAS_REF = {'第01章', '第02章', '第03章', '第04章'}

# 样张说明 (sample explanation for Ch1)
YANGZHANG = """> **关于"章后产出物"**
>
> 本书每一章结尾都附有与该章叙事相关的虚构文件——合约、申诉记录、听证纪要、制度草案等。它们不是注释，也不是附录摘要；它们本身就是故事的一部分，是"制度如何从人的疼痛中长出来"的实物证据。
>
> 以下是第01章的完整产出物样张。自第02章起，所有章后产出物均已移至同目录下的独立文件（文件名格式：`第XX章_标题-产出物.md`），以便阅读时自由选择：先读完全部正文，再集中翻阅工件；或每章读完即翻。"""


def main():
    # ── Read main file ──────────────────────────────────────────────
    with open(MAIN, 'r', encoding='utf-8-sig') as f:
        text = f.read()
    lines = text.split('\n')
    print(f"Read {len(lines)} lines from main file.")

    # ── Locate 产出物 sections ──────────────────────────────────────
    art_re = re.compile(r'^# (第\d{2}章|彩蛋章)：.+ — 章后产出物')
    h1_indices = [i for i, L in enumerate(lines) if L.startswith('# ')]

    artifacts = []
    for i, L in enumerate(lines):
        m = art_re.match(L)
        if m:
            ch_id = m.group(1)
            # End = next H1 heading (or EOF)
            end = len(lines)
            for h1 in h1_indices:
                if h1 > i:
                    end = h1
                    break
            artifacts.append({'id': ch_id, 'start': i, 'end': end})

    print(f"\nFound {len(artifacts)} 产出物 sections:")
    for a in artifacts:
        print(f"  {a['id']}: L{a['start']+1} – L{a['end']}")

    if len(artifacts) != 25:
        print(f"WARNING: Expected 25, got {len(artifacts)}")

    # ── Step 1: Write standalone files ──────────────────────────────
    print("\n── Writing standalone files ──")
    for art in artifacts:
        ch = art['id']
        if ch == '第01章':
            print(f"  SKIP {FILEMAP[ch]} (Ch1 stays inline)")
            continue
        if ch in C_TRIMMED:
            print(f"  SKIP {FILEMAP[ch]} (C-trimmed, keep existing full version)")
            continue

        content = '\n'.join(lines[art['start']:art['end']]).rstrip() + '\n'
        path = os.path.join(BASE, FILEMAP[ch])
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  WROTE {FILEMAP[ch]}  ({len(content)} chars)")

    # ── Step 2: Rebuild main file ───────────────────────────────────
    print("\n── Rebuilding main file ──")

    # Find Ch1's existing reference line (to remove it)
    ch1_ref = None
    for i, L in enumerate(lines):
        if '章后产出物见' in L and '第01章' in L:
            ch1_ref = i
            break
    if ch1_ref is not None:
        print(f"  Ch1 ref line found at L{ch1_ref+1}, will be removed.")

    # Build segments: (start, end, type, chapter_id)
    sorted_arts = sorted(artifacts, key=lambda a: a['start'])
    segments = []
    prev = 0
    for art in sorted_arts:
        if art['start'] > prev:
            segments.append((prev, art['start'], 'text', None))
        segments.append((art['start'], art['end'], 'artifact', art['id']))
        prev = art['end']
    if prev < len(lines):
        segments.append((prev, len(lines), 'text', None))

    # Process segments
    output = []
    for start, end, seg_type, ch_id in segments:
        if seg_type == 'text':
            # Copy text lines, removing Ch1's old reference line
            for j in range(start, end):
                if j == ch1_ref:
                    continue
                output.append(lines[j])

        elif seg_type == 'artifact':
            if ch_id == '第01章':
                # Insert 样张说明, then keep 产出物 inline
                # Trim trailing blanks
                while output and output[-1].strip() == '':
                    output.pop()
                output.append('')
                for yang_line in YANGZHANG.split('\n'):
                    output.append(yang_line)
                output.append('')
                # Keep the actual 产出物 content
                for j in range(start, end):
                    output.append(lines[j])
            else:
                # ── Replace with reference line ─────────────────────
                fname = FILEMAP[ch_id]

                if ch_id not in HAS_REF:
                    # Ch5+: add --- + reference line
                    while output and output[-1].strip() == '':
                        output.pop()
                    if output and output[-1].strip() != '---':
                        output.append('')
                        output.append('---')
                    output.append('')
                    output.append(f'> 章后产出物见：`{fname}`')
                    output.append('')
                # else: Ch2-4 already have reference lines in preceding text

                # Special: Ch24 contains （正文完） separator → preserve it
                if ch_id == '第24章':
                    for j in range(start, end):
                        if '正文完' in lines[j]:
                            output.append('')
                            output.append('---')
                            output.append('')
                            output.append(lines[j])   # > **（正文完）**
                            output.append('')
                            output.append('---')
                            output.append('')
                            break

    # ── Clean up: collapse 3+ consecutive blank lines to 2 ─────────
    result = '\n'.join(output)
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    # Ensure file ends with single newline
    result = result.rstrip('\n') + '\n'

    with open(MAIN, 'w', encoding='utf-8') as f:
        f.write(result)

    new_count = result.count('\n') + 1
    print(f"\n── Done ──")
    print(f"  Main file: {len(lines)} → {new_count} lines")
    print(f"  Standalone files written: {25 - 1 - len(C_TRIMMED)} new + {len(C_TRIMMED)} kept")


if __name__ == '__main__':
    main()
