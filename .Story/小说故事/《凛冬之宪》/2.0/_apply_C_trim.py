# -*- coding: utf-8 -*-
"""C-type trim: condense lower-tension artifacts in Ch21-Ch25.
Uses line-range replacement to avoid curly-quote matching issues."""

import os

FILE = os.path.join(os.path.dirname(__file__),
                    'ASTO.凛冬之宪--艰难的前进历程.md')

with open(FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0

def trim_range(start, end, new_lines, label):
    """Replace lines[start-1:end] (1-indexed) with new_lines."""
    global lines, count
    # Verify anchor text
    anchor = lines[start - 1].strip()
    print(f"  Anchor L{start}: {anchor[:60]}...")
    lines[start - 1:end] = [l + '\n' for l in new_lines]
    count += 1
    print(f"  [{count}] {label}: replaced L{start}-L{end} ({end-start+1} lines -> {len(new_lines)} lines)")


# ============================================================
# Ch22 [B] 分叉机制: L6543-L6560 (header through ---)
# ============================================================
trim_range(6543, 6560, [
    '## [B \u8865\u4e01]\u300a\u5b9a\u671f\u5206\u53c9\u4e0e\u56de\u5f52\u673a\u5236\uff08\u8bd5\u884c\uff09\u300b',
    '',
    '> \u6587\u4ef6\u7f16\u53f7\uff1aFORK-RETURN-TRIAL',
    '> \u6458\u8981\uff1a\u6bcf\u5e741\u6708\u7528\u6237\u53ef\u7533\u8bf7\u8131\u79bb\u4e3b\u7f91\u4e00\u5468\uff1b\u56de\u5f52\u65f6\u4e0d\u6b67\u89c6\u3001\u4e0d\u964d\u7ea7\u3002\u5f81\u6c42\u610f\u89c1\u7a3f\u4e0a\u5199\u6ee1\u6279\u6ce8\u2014\u2014\u201c\u592a\u6fc0\u8fdb\u4e86\u201d\u548c\u201c\u592a\u4fdd\u5b88\u4e86\u201d\u5e76\u5217\u3002',
    '> *\uff08\u5b8c\u6574\u5de5\u4ef6\u89c1\u6863\u6848\u7d22\u5f15\uff09*',
    '',
    '---',
], 'Ch22 [B] \u5206\u53c9\u673a\u5236 \u538b\u7f29')


# ============================================================
# Ch22 [C] 理论堆肥: L6562-L6580 (header through ---)
# After previous trim, line numbers shifted. Recalculate.
# Original L6562 is now at 6543 + 7 (new lines) = 6550
# But easier: search for the anchor text
# ============================================================
# Find new position of 理论堆肥
for i, line in enumerate(lines):
    if '\u7406\u8bba\u5806\u80a5\u516c\u544a v1.0' in line and '## [C' in line:
        compost_start = i + 1  # 1-indexed
        break

# Find the next --- after it
for j in range(compost_start, len(lines)):
    if lines[j].strip() == '---' and j > compost_start + 2:
        compost_end = j + 1  # 1-indexed, inclusive
        break

trim_range(compost_start, compost_end, [
    '## [C \u5236\u5ea6]\u300a\u7406\u8bba\u5806\u80a5\u516c\u544a v1.0\u300b',
    '',
    '> \u6587\u4ef6\u7f16\u53f7\uff1aTHEORY-COMPOST-1.0',
    '> \u6458\u8981\uff1a\u8bbe\u7acb\u201c\u7406\u8bba\u5806\u80a5\u533a\u201d\u2014\u2014\u9519\u8bef\u7684\u7406\u8bba\u4e0d\u5220\u9664\uff0c\u6253\u5370\u6295\u5165\u5b9e\u4f53\u5806\u80a5\u7bb1\uff0c\u8ba9\u5b83\u4eec\u8150\u70c2\u6210\u517b\u5206\u3002',
    '> *\uff08\u5b8c\u6574\u5de5\u4ef6\u89c1\u6863\u6848\u7d22\u5f15\uff09*',
    '',
    '---',
], 'Ch22 [C] \u7406\u8bba\u5806\u80a5 \u538b\u7f29')


# ============================================================
# Ch23 [C] 公开听证纪要
# ============================================================
for i, line in enumerate(lines):
    if '\u516c\u5f00\u542c\u8bc1\u7eaa\u8981\uff08\u6b63\u5f0f\u5f52\u6863\uff09' in line and '## [C' in line:
        hearing_start = i + 1
        break

for j in range(hearing_start, len(lines)):
    if lines[j].strip() == '---' and j > hearing_start + 2:
        hearing_end = j + 1
        break

trim_range(hearing_start, hearing_end, [
    '## [C \u5236\u5ea6]\u300a\u516c\u5f00\u542c\u8bc1\u7eaa\u8981\uff08\u6b63\u5f0f\u5f52\u6863\uff09\u300b',
    '',
    '> \u6587\u4ef6\u7f16\u53f7\uff1aHEARING-MINUTES-ARCHIVE',
    '> \u6458\u8981\uff1a\u51b3\u8bae\u4e09\u6761\u2014\u2014\u4e0d\u63a9\u76d6\u6f0f\u6d1e\u3001\u5e9f\u9664\u201c\u7edd\u5bf9\u65f6\u6548\u6027\u201d\u3001\u786e\u7acb\u201c\u6548\u7387\u670d\u52a1\u4e8e\u516c\u6b63\u201d\u539f\u5219\u3002',
    '> *\uff08\u5b8c\u6574\u5de5\u4ef6\u89c1\u6863\u6848\u7d22\u5f15\uff09*',
    '',
    '---',
], 'Ch23 [C] \u542c\u8bc1\u7eaa\u8981 \u538b\u7f29')


# ============================================================
# Ch24 [B] 退出权再确认通知
# ============================================================
for i, line in enumerate(lines):
    if '\u9000\u51fa\u6743\u518d\u786e\u8ba4\u901a\u77e5' in line and '## [B' in line:
        exit_start = i + 1
        break

# Find next --- after it
for j in range(exit_start, len(lines)):
    if lines[j].strip() == '---' and j > exit_start + 2:
        exit_end = j + 1
        break

trim_range(exit_start, exit_end, [
    '## [B \u8865\u4e01]\u300a\u9000\u51fa\u6743\u518d\u786e\u8ba4\u901a\u77e5\uff08\u9ad8\u6469\u64e6\u8bbe\u8ba1\uff09\u300b',
    '',
    '> \u6587\u4ef6\u7f16\u53f7\uff1aEXIT-RECONFIRM-0.1',
    '> \u6458\u8981\uff1a\u9000\u51fa\u6309\u94ae\u6539\u4e3a\u7070\u8272\u3001\u957f\u63095\u79d2\u89e6\u53d1\u300148\u5c0f\u65f6\u540e\u6094\u671f\u3002\u754c\u9762\u540c\u65f6\u5217\u51fa\u4f60\u5c06\u5931\u53bb\u7684\uff08\u76d1\u6d4b\u3001\u8f85\u52a9\u3001\u80cc\u4e66\uff09\u548c\u4f60\u5c06\u83b7\u5f97\u7684\uff08\u9690\u79c1\u3001\u72af\u9519\u7684\u81ea\u7531\u3001\u5b64\u72ec\u7684\u6743\u5229\uff09\u3002',
    '> *\uff08\u5b8c\u6574\u5de5\u4ef6\u89c1\u6863\u6848\u7d22\u5f15\uff09*',
    '',
    '---',
], 'Ch24 [B] \u9000\u51fa\u6743\u901a\u77e5 \u538b\u7f29')


# ============================================================
print(f"\n=== C-trim: {count} artifacts condensed ===")

with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("C changes written to file.")
