"""
重新生成合订版 Book 文件
将108篇故事按编号顺序合并为一个 Markdown 文件
"""
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
BOOK_PATH = os.path.join(BASE, 'ASTO.思维越狱的108个世纪谜题_Book_v1.0.md')


def get_story_files():
    pattern = os.path.join(BASE, 'ASTO.S[0-9]*.md')
    files = glob.glob(pattern)
    result = []
    for f in files:
        bn = os.path.basename(f)
        m = re.search(r'S(\d+)', bn)
        if m:
            num = int(m.group(1))
            if num == 0:
                continue
            result.append((num, f, bn))
    result.sort()
    return result


def main():
    files = get_story_files()
    print(f'找到 {len(files)} 篇故事')

    # 读取序言结语
    preface_path = os.path.join(BASE, 'ASTO.Book.序言与结语.md')
    preface = ''
    if os.path.exists(preface_path):
        with open(preface_path, 'r', encoding='utf-8') as f:
            preface = f.read().strip()

    # 构建目录
    toc_lines = []
    for num, fp, bn in files:
        name = bn.replace('.md', '').replace('ASTO.', '')
        toc_lines.append(f'- {bn.replace(".md", "")}')

    # 构建合订版
    parts = []
    parts.append('# 《ASTO · 一百零八问》：划下那一刀')
    parts.append('> 合订版（当前收录：108 篇，ASTO.S001–ASTO.S108）')
    parts.append('> 单篇正文可按同目录 ASTO.S001…（持续更新）分篇阅读；序言 + 结语见：ASTO.Book.序言与结语.md。')
    parts.append('')
    parts.append('## 目录（按文件顺序）')
    parts.extend(toc_lines)
    parts.append('')

    # 写作纪律补丁
    parts.append('## 写作纪律补丁：回流 / 螺旋 / Residue')
    parts.append('- **回流/递归**：状态不保证单向推进；压力上来时，人会退回更原始的习惯与解释框架。写作上要让"回滚/降级/撤回"成为可执行动作，而不是失败宣言。')
    parts.append('- **螺旋回归**：你会反复遇到同一类问题，但每一次都会携带上一轮的经验与偏差；不要写成"回到原样/命中注定"。')
    parts.append('- **Residue（剩馀物/代价）**：每一次切割都会留下剩馀物——遗憾、关系成本、时间损耗、名声划痕；要把它写进账里，避免把选择包装成"无代价的正确"。')
    parts.append('- **封板不"中性"**：任何"我决定了"都是一次版本冻结；它可能需要复盘、需要重开、需要在更高分辨率下改写。封板的价值是行动，不是永恒正确。')
    parts.append('')

    # 序言
    if preface:
        parts.append('---')
        parts.append('')
        parts.append(preface)
        parts.append('')

    # 正文
    for num, fp, bn in files:
        parts.append('---')
        parts.append('')
        with open(fp, 'r', encoding='utf-8') as f:
            story = f.read().strip()
        parts.append(story)
        parts.append('')

    content = '\n'.join(parts)

    with open(BOOK_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'合订版已生成: {os.path.basename(BOOK_PATH)}')
    print(f'总字符数: {len(content):,}')


if __name__ == '__main__':
    main()
