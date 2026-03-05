MAIN = r'D:\_Progs\01Center\ASTO\小说故事\《凛冬之宪》\2.0\ASTO.凛冬之宪--艰难的前进历程.md'

with open(MAIN, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Targets: (line_number, old_fragment, new_fragment)
targets = [
    # L587: system file reference dropdown — remove trailing version
    (587,
     'EPO-2040-01-12-0001《紧急保护令（临时补丁）》v0.0.1',
     'EPO-2040-01-12-0001《紧急保护令（临时补丁）》'),
    # L617: form field — remove version from file ref
    (617,
     '- 关联文件：EPO-2040-01-12-0001 v0.0.1',
     '- 关联文件：EPO-2040-01-12-0001'),
    # L646: receipt description — remove the v0.0.1 echo
    (646,
     '回执上同样有那行字：v0.0.1。',
     '回执的纸角还带着打印机的热。'),
    # L672: Shen sees the paper — remove version echo
    (672,
     '右上角：v0.0.1。',
     '右上角的墨很淡，像印得太急。'),
    # L1151: Ch3 — remove version from narrative ref
    (1151,
     '他把那张 v0.0.1 的回执再次翻过来',
     '他把那张回执再次翻过来'),
]

count = 0
for lnum, old, new in targets:
    idx = lnum - 1
    if old in lines[idx]:
        lines[idx] = lines[idx].replace(old, new, 1)
        count += 1
        print(f'  OK L{lnum}')
    else:
        print(f'  MISS L{lnum}: looking for [{old[:40]}]')

with open(MAIN, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Reduced v0.0.1 in {count} places')
