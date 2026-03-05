import re

MAIN = r'D:\_Progs\01Center\ASTO\小说故事\《凛冬之宪》\2.0\ASTO.凛冬之宪--艰难的前进历程.md'

with open(MAIN, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Target lines (1-indexed) and what to replace
# Format: (line_number, old_fragment, new_fragment)
targets = [
    (135, '**让人类把错误承担清楚**', '让人类把错误承担清楚'),
    (311, '**紧急刹车不是为了让你永远正确。它是为了让你在错误发生后，仍然必须看见。**',
          '紧急刹车不是为了让你永远正确。它是为了让你在错误发生后，仍然必须看见。'),
    (535, '**梁雪**', '梁雪'),
    (730, '**谁可以问、怎么问、问完之后谁必须回答。**', '谁可以问、怎么问、问完之后谁必须回答。'),
    (766, '**申诉入口**', '申诉入口'),
    (782, '**护栏不是为了让你永远正确。护栏是为了让你错了也得认。**',
          '护栏不是为了让你永远正确。护栏是为了让你错了也得认。'),
    (834, '**谁必须回答**', '谁必须回答'),
]

count = 0
for lnum, old, new in targets:
    idx = lnum - 1
    if old in lines[idx]:
        lines[idx] = lines[idx].replace(old, new, 1)
        count += 1
        print(f'  OK L{lnum}: {old[:30]}...')
    else:
        print(f'  MISS L{lnum}: {old[:30]}...')

with open(MAIN, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Removed bold from {count} narrative lines')
