import os

MAIN = r'D:\_Progs\01Center\ASTO\小说故事\《凛冬之宪》\2.0\ASTO.凛冬之宪--艰难的前进历程.md'
DIR = r'D:\_Progs\01Center\ASTO\小说故事\《凛冬之宪》\2.0'

with open(MAIN, 'r', encoding='utf-8-sig') as f:
    text = f.read()

files = [
    '第02章_沈知行的选择-产出物.md',
    '第06章_被遗忘的小镇-产出物.md',
    '第14章_危机的焊接-产出物.md',
    '第17章_逆熵智能体-产出物.md',
    '第18章_最后一次警告-产出物.md',
    '第22章_未完成清单-产出物.md',
]

BT = chr(96)  # backtick
count = 0
for fname in files:
    ref_line = '> 章后产出物见：' + BT + fname + BT
    if ref_line not in text:
        print(f'  SKIP {fname} - ref line not found')
        continue

    fpath = os.path.join(DIR, fname)
    with open(fpath, 'r', encoding='utf-8-sig') as f:
        content = f.read().replace('\r\n', '\n').rstrip('\n')

    text = text.replace(ref_line, content)
    count += 1
    print(f'  OK {fname}')

with open(MAIN, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Restored {count} artifacts inline')
