"""
《思维越狱》批量优化脚本
P0: 全量追加回流预警
P1a: ASTO介入段落去重
P1b: 急救包物理动词检查（仅报告）
P2: 全量幕次编号检查（仅报告）
"""
import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── 配置 ───────────────────────────────────────────

REFLOW_WARNING = (
    "\n> **⚠️ 回流预警**：过几天，他/她可能会再次卡住。\n"
    "> 那不是失败，那是系统在做压力测试。\n"
    "> 区别在于：这一次，他/她知道急救包在哪。\n"
)

# ASTO通用介入段落的正则（匹配多种变体）
ASTO_GENERIC_BLOCK = re.compile(
    r'(在这里，\*\*ASTO（属集变迁存在论）\*\*\s*介入了。\s*\n'
    r'(?:\s*\n)*'
    r'它的核心定义很简单：\s*\n?'
    r'\*\*世上没有一成不变的"东西"（实体），只有暂时聚在一起的"特征包"（属性集合）。\*\*\s*\n?'
    r'(?:所有的"存在"，本质上都是这个集合在时间长河中的一次次\*\*版本更新（变迁）\*\*。\s*\n?)?)',
    re.MULTILINE
)

# 也匹配单行紧凑变体
ASTO_GENERIC_COMPACT = re.compile(
    r'(在这里，\*\*ASTO（属集变迁存在论）\*\*\s*介入了。\s*\n'
    r'(?:\s*\n)*'
    r'它的核心定义很简单：\s*'
    r'\*\*世上没有一成不变的"东西"（实体），只有暂时聚在一起的"特征包"（属性集合）。\*\*\s*\n?'
    r'(?:所有的"存在"，本质上都是这个集合在时间长河中的一次次\*\*版本更新（变迁）\*\*。\s*\n?)?)',
    re.MULTILINE
)

# 它认为的变体（部分后期文章用了不同的引入句式）
ASTO_ALT_BLOCK = re.compile(
    r'(在这里，\*\*ASTO（属集变迁存在论）\*\*\s*介入了。\s*\n'
    r'(?:\s*\n)*'
    r'它认为：\s*\n)',
    re.MULTILINE
)

# 急救包物理动词列表
PHYSICAL_VERBS = [
    '写', '走', '打', '拿', '关', '扔', '撕', '站', '拨', '拉', '推', '放',
    '喝', '吃', '做', '买', '卖', '跑', '搬', '整理', '清', '擦', '叠',
    '拍', '画', '摸', '闻', '听', '看', '翻', '掏', '贴', '剪', '揉',
    '握', '按', '打开', '关掉', '删除', '发送', '输入', '搜索', '设',
    '记', '标记', '称', '量', '找', '问', '告诉', '声明', '说',
    '承认', '自问', '下载', '安装', '卸载', '注销', '屏蔽', '拉黑',
    '给', '寄', '买', '取消', '退订', '解绑', '用',
]

# 卷首篇检测（需要保留完整 ASTO 介入的篇目）
# 通过实际读取文件中的卷别标记来判断是否为卷首篇
def is_volume_opener(content, num):
    """检查是否为卷首篇（卷别标注中序号为1）"""
    if num <= 3:
        return True  # S001-S003 始终保留完整版
    m = re.search(r'卷.+?·.+?\((\d+)/\d+\)', content)
    if m and m.group(1) == '1':
        return True
    # 也检查没有 (x/y) 标记但内容暗示是卷首的情况
    return False


def get_story_files():
    """获取所有故事文件，按编号排序"""
    pattern = os.path.join(BASE, "ASTO.S[0-9]*.md")
    files = glob.glob(pattern)
    result = []
    for f in files:
        bn = os.path.basename(f)
        m = re.search(r'S(\d+)', bn)
        if m:
            num = int(m.group(1))
            if num == 0:  # 跳过模板
                continue
            result.append((num, f))
    result.sort()
    return result


def insert_reflow_warning(content):
    """P0: 在急救包之前插入回流预警"""
    # 查找急救包标题行的多种变体
    patterns = [
        r'(---\s*\n\s*\n##\s*第七幕[｜|]?\s*🛠️\s*急救包)',
        r'(---\s*\n\s*\n##\s*🛠️\s*ASTO\s*急救包)',
        r'(---\s*\n\s*\n##\s*第七幕[｜|]?\s*🛠️\s*ASTO\s*急救包)',
        r'(---\s*\n\s*\n##\s*第三幕[｜|]?\s*🛠️\s*急救包)',  # S096的变体
    ]
    
    for pat in patterns:
        m = re.search(pat, content)
        if m:
            insert_pos = m.start()
            # 在 --- 之前插入回流预警
            return content[:insert_pos] + "\n" + REFLOW_WARNING + "\n" + content[insert_pos:], True
    
    # 兜底：直接搜索 "急救包" 标题
    m = re.search(r'(##\s*(?:第[一二三四五六七八九十]+幕)?[｜|]?\s*🛠️\s*(?:ASTO\s*)?急救包)', content)
    if m:
        # 找到该行所在的 --- 分隔符
        line_start = content.rfind('\n---', 0, m.start())
        if line_start > 0:
            insert_pos = line_start
            return content[:insert_pos] + "\n" + REFLOW_WARNING + "\n" + content[insert_pos:], True
        else:
            insert_pos = m.start()
            return content[:insert_pos] + REFLOW_WARNING + "\n" + content[insert_pos:], True
    
    return content, False


def dedup_asto_intro(content, num):
    """P1a: ASTO介入段落去重"""
    if num <= 3:
        return content, False  # S001-S003 保持原样
    
    if is_volume_opener(content, num):
        return content, False  # 卷首篇保持完整
    
    # 尝试匹配并替换
    for pattern in [ASTO_GENERIC_BLOCK, ASTO_GENERIC_COMPACT]:
        m = pattern.search(content)
        if m:
            if num <= 18:
                # S004-S018: 缩减为一行引用
                replacement = "ASTO 介入。（核心前提见 S001：没有实体，只有属性集合。）\n\n"
            else:
                # S019+: 直接省略通用定义
                replacement = "**ASTO** 介入——\n\n"
            content = content[:m.start()] + replacement + content[m.end():]
            return content, True
    
    return content, False


def check_emergency_kit(content, num):
    """P1b: 检查急救包第4条是否包含物理动词"""
    # 找到急救包部分
    kit_start = re.search(r'##\s*(?:第[一二三四五六七八九十]+幕)?[｜|]?\s*🛠️', content)
    if not kit_start:
        return None
    
    # 找到急救包之后的内容（到下一个 ## 或 --- 为止）
    kit_text = content[kit_start.start():]
    next_section = re.search(r'\n##\s', kit_text[10:])
    if next_section:
        kit_text = kit_text[:next_section.start() + 10]
    
    # 提取所有编号条目
    items = re.findall(r'\d+\.\s+\*\*(.+?)\*\*[：:](.+?)(?=\n\d+\.|\n>|\n---|\Z)', kit_text, re.DOTALL)
    
    if len(items) < 4:
        # 尝试另一种格式
        items = re.findall(r'\d+\.\s+\*\*(.+?)\*\*', kit_text)
    
    if len(items) >= 4:
        last_item_label = items[3] if isinstance(items[3], str) else items[3][0]
        # 获取第4条的完整文本
        fourth_match = re.findall(r'4\.\s+(.+?)(?=\n\n|\n>|\n---|\Z)', kit_text, re.DOTALL)
        fourth_text = fourth_match[0] if fourth_match else last_item_label
        
        # 检查是否包含物理动词
        has_physical = any(v in fourth_text for v in PHYSICAL_VERBS)
        if not has_physical:
            return f"S{num:03d} 急救包第4条可能缺少物理动词: {fourth_text[:60]}..."
    
    return None


def check_act_numbers(content, num):
    """P2: 检查幕次编号是否有重复或乱序"""
    acts = re.findall(r'##\s*(第[一二三四五六七八九十]+幕)', content)
    issues = []
    
    # 检查重复
    seen = {}
    for act in acts:
        if act in seen:
            issues.append(f"S{num:03d} 幕次重复: {act}")
        seen[act] = seen.get(act, 0) + 1
    
    return issues


def main():
    files = get_story_files()
    print(f"找到 {len(files)} 个故事文件\n")
    
    reflow_count = 0
    dedup_count = 0
    kit_issues = []
    act_issues = []
    
    for num, filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # P0: 回流预警
        content, reflow_added = insert_reflow_warning(content)
        if reflow_added:
            reflow_count += 1
        
        # P1a: ASTO介入去重
        content, dedup_done = dedup_asto_intro(content, num)
        if dedup_done:
            dedup_count += 1
        
        # P1b: 急救包检查（仅报告）
        issue = check_emergency_kit(content, num)
        if issue:
            kit_issues.append(issue)
        
        # P2: 幕次编号检查（仅报告）
        act_issue = check_act_numbers(content, num)
        act_issues.extend(act_issue)
        
        # 写回文件（如果有修改）
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
    
    # 输出报告
    print("=" * 60)
    print("优化执行报告")
    print("=" * 60)
    print(f"\n[P0] 回流预警: 成功插入 {reflow_count}/{len(files)} 篇")
    print(f"[P1a] ASTO介入去重: 成功处理 {dedup_count}/{len(files)} 篇")
    
    print(f"\n[P1b] 急救包物理动词问题 ({len(kit_issues)} 条):")
    for issue in kit_issues:
        print(f"  - {issue}")
    
    print(f"\n[P2] 幕次编号问题 ({len(act_issues)} 条):")
    for issue in act_issues:
        print(f"  - {issue}")
    
    print("\n完成。")


if __name__ == '__main__':
    main()
