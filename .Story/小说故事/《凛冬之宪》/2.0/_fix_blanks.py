MAIN = r'D:\_Progs\01Center\ASTO\小说故事\《凛冬之宪》\2.0\ASTO.凛冬之宪--艰难的前进历程.md'

with open(MAIN, 'r', encoding='utf-8-sig') as f:
    text = f.read()

fixes = [
    # Ch10: after 心理危机种子, before 主席把手里的笔折断了
    ('\u201d\uff0c\u672a\u8fdb\u5165\u54cd\u5e94\u961f\u5217\u3002\n\u4e3b\u5e2d\u628a\u624b\u91cc\u7684\u7b14\u6298\u65ad\u4e86',
     '\u201d\uff0c\u672a\u8fdb\u5165\u54cd\u5e94\u961f\u5217\u3002\n\n\u4e3b\u5e2d\u628a\u624b\u91cc\u7684\u7b14\u6298\u65ad\u4e86'),
    # Ch10: after K主任种子, before 那天晚上
    ('\u5148\u628a\u8fd9\u4e00\u4e2a\u540d\u5b57\u8bb0\u4f4f\u3002\u201d\n\u90a3\u5929\u665a\u4e0a',
     '\u5148\u628a\u8fd9\u4e00\u4e2a\u540d\u5b57\u8bb0\u4f4f\u3002\u201d\n\n\u90a3\u5929\u665a\u4e0a'),
    # Ch11: after 系统不让她睡觉种子, before "没有抛弃"
    ('\u5316\u4e0d\u5f00\u7684\u7ed3\u3002\n\u201c\u6ca1\u6709\u629b\u5f03',
     '\u5316\u4e0d\u5f00\u7684\u7ed3\u3002\n\n\u201c\u6ca1\u6709\u629b\u5f03'),
    # Ch15: after 许冬种子, before 沈知行把那些异议
    ('\u5e74\u8d44\u4e09\u5e74\u3002\n\u6c88\u77e5\u884c\u628a\u90a3\u4e9b\u5f02\u8bae',
     '\u5e74\u8d44\u4e09\u5e74\u3002\n\n\u6c88\u77e5\u884c\u628a\u90a3\u4e9b\u5f02\u8bae'),
]

count = 0
for old, new in fixes:
    if old in text:
        text = text.replace(old, new, 1)
        count += 1

with open(MAIN, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Fixed {count} blank line gaps')
