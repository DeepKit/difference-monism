"""
《思维越狱》P1a+P2 批量优化脚本（第二轮）
- P1a: ASTO介入段落去重
- P2: 修复幕次重复
"""
import os, re, glob, sys

sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))


def get_story_files():
    pattern = os.path.join(BASE, "ASTO.S[0-9]*.md")
    files = glob.glob(pattern)
    result = []
    for f in files:
        bn = os.path.basename(f)
        m = re.search(r'S(\d+)', bn)
        if m:
            num = int(m.group(1))
            if num == 0:
                continue
            result.append((num, f))
    result.sort()
    return result


def is_volume_opener(content, num):
    """检查是否为卷首篇"""
    if num <= 3:
        return True
    # 匹配 (1/18) 或 (1/12) 等
    m = re.search(r'\(1/\d+\)', content[:500])
    if m:
        return True
    return False


def dedup_asto_intro(content, num):
    """P1a: ASTO介入段落去重"""
    if num <= 3:
        return content, False, "保留(S001-003)"
    if is_volume_opener(content, num):
        return content, False, "保留(卷首篇)"

    # 标准三行块（有换行分隔）
    # 在这里，**ASTO（属集变迁存在论）** 介入了。
    # \n
    # 它的核心定义很简单：
    # **世上没有...** 
    # [可选: 所有的"存在"...]
    pattern = (
        r'在这里，\*\*ASTO（属集变迁存在论）\*\*\s*介入了。\s*\n'
        r'\s*\n'
        r'它的核心定义很简单[：:]\s*\n'
        r'\*\*世上没有一成不变的["\u201c]东西["\u201d]（实体），只有暂时聚在一起的["\u201c]特征包["\u201d]（属性集合）。\*\*\s*\n'
        r'(?:所有的["\u201c]存在["\u201d]，本质上都是这个集合在时间长河中的一次次\*\*版本更新（变迁）\*\*。\s*\n)?'
    )

    m = re.search(pattern, content)
    if m:
        if num <= 18:
            replacement = 'ASTO 介入。（核心前提见 S001：没有实体，只有属性集合。）\n\n'
        else:
            replacement = '**ASTO** 介入——\n\n'
        content = content[:m.start()] + replacement + content[m.end():]
        return content, True, "去重成功"

    # 紧凑变体：核心定义和粗体在同一行
    pattern2 = (
        r'在这里，\*\*ASTO（属集变迁存在论）\*\*\s*介入了。\s*\n'
        r'\s*\n'
        r'它的核心定义很简单[：:]\s*'
        r'\*\*世上没有一成不变的["\u201c]东西["\u201d]（实体），只有暂时聚在一起的["\u201c]特征包["\u201d]（属性集合）。\*\*\s*\n'
        r'(?:所有的["\u201c]存在["\u201d]，本质上都是这个集合在时间长河中的一次次\*\*版本更新（变迁）\*\*。\s*\n)?'
    )

    m = re.search(pattern2, content)
    if m:
        if num <= 18:
            replacement = 'ASTO 介入。（核心前提见 S001：没有实体，只有属性集合。）\n\n'
        else:
            replacement = '**ASTO** 介入——\n\n'
        content = content[:m.start()] + replacement + content[m.end():]
        return content, True, "去重成功(紧凑)"

    # "它认为："变体（S096等后期篇目用了不同句式，不含通用定义——跳过）
    return content, False, "未匹配"


def fix_duplicate_acts(content, num):
    """P2: 修复重复的第三幕"""
    acts = [(m.start(), m.group(1)) for m in re.finditer(r'##\s*(第[一二三四五六七八九十]+幕)', content)]
    
    seen = {}
    fixes = []
    for pos, act in acts:
        if act in seen:
            fixes.append((pos, act, seen[act]))
        seen[act] = pos
    
    if not fixes:
        return content, False
    
    # 对于重复的第三幕：通常第一个是知识卡片后的"图层错误发现"，第二个是ASTO降维打击
    # 需要具体看上下文来决定怎么修
    # 常见情况：S005-S013有两个"第三幕"，第二个应该是"第四幕"
    # S096 有两个"第三幕"
    modified = False
    offset = 0
    
    for pos, act, first_pos in fixes:
        adj_pos = pos + offset
        if act == '第三幕':
            # 查看第二个第三幕后面的内容来决定改成什么
            context = content[adj_pos:adj_pos+200]
            if '急救包' in context or '🛠️' in context:
                new_act = '第七幕'
            elif 'ASTO' in context and ('降维' in context or '介入' in context):
                new_act = '第四幕'
            elif '地图错了' in context or '图层错误' in context:
                # 第二个才是图层错误发现，第一个可能标错了
                new_act = '第三幕'  # 保持不变
                continue
            else:
                new_act = '第四幕'  # 默认改为第四幕
            
            old_text = f'## {act}'
            new_text = f'## {new_act}'
            # 精确替换这个位置的文本
            before = content[:adj_pos]
            after = content[adj_pos:]
            after = after.replace(old_text, new_text, 1)
            content = before + after
            modified = True
            print(f"  S{num:03d}: {act} -> {new_act}")
    
    return content, modified


def main():
    files = get_story_files()
    print(f"找到 {len(files)} 个故事文件\n")

    dedup_count = 0
    dedup_skip = 0
    dedup_fail = 0
    act_fix_count = 0

    for num, filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # P1a
        content, done, reason = dedup_asto_intro(content, num)
        if done:
            dedup_count += 1
        elif '保留' in reason:
            dedup_skip += 1
        else:
            dedup_fail += 1
            if num <= 50:  # 只报告前50个的失败
                print(f"  [P1a] S{num:03d} 未匹配: {reason}")

        # P2
        content, act_fixed = fix_duplicate_acts(content, num)
        if act_fixed:
            act_fix_count += 1

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    print(f"\n{'='*60}")
    print(f"[P1a] ASTO去重: 成功={dedup_count}, 保留={dedup_skip}, 未匹配={dedup_fail}")
    print(f"[P2]  幕次修复: {act_fix_count} 篇")
    print("完成。")


if __name__ == '__main__':
    main()
