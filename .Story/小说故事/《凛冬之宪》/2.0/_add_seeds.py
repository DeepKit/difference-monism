MAIN = r'D:\_Progs\01Center\ASTO\小说故事\《凛冬之宪》\2.0\ASTO.凛冬之宪--艰难的前进历程.md'

with open(MAIN, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Insertions: (after_line_number, text_to_insert)
# MUST be in REVERSE order (largest line number first) to avoid shifting issues

insertions = [
    # 4. Ch15 L4265: 许冬提及 (after the翻译员 line)
    (4266, [
        '\n',
        '其中有一条异议没有署真名。提交者只填了工号，后面写着一句话：\n',
        '\n',
        '\u201c如果系统能预测一个人会死，但无法让她活得像人，那这个系统在保护什么？\u201d\n',
        '\n',
        '姬可后来调了提交日志。工号对应的名字叫许冬，心理干预组，年资三年。\n',
    ]),
    # 3. Ch11 L3459: "系统不让她睡觉" (after "冰得像石头。")
    (3460, [
        '\n',
        '走廊另一头，一个穿病号服的老人拽住路过的护士。\n',
        '\n',
        '\u201c你们那个系统，\u201d她说，声音像一根快断的弦，\u201c每天夜里都给我发提醒。说我心率不对。我越看越睡不着，越睡不着它越提醒。\u201d\n',
        '\n',
        '护士安慰了几句，把她扶回病房。\n',
        '\n',
        '但那句\u201c越睡不着它越提醒\u201d留在走廊里，像一团化不开的结。\n',
    ]),
    # 2. Ch10 L3341: K主任种子 (after "别让她的名字只变成 0.91 里的一个分母。")
    (3342, [
        '\n',
        '有人补了一句：\u201cK主任那边在做一个预判模型，说准确率能到99%以上。以后也许就不会\u2014\u2014\u201d\n',
        '\n',
        '主席打断他：\u201c以后的事以后说。先把这一个名字记住。\u201d\n',
    ]),
    # 1. Ch10 L3293: 心理危机种子 (after "她的选择……是意外。")
    (3294, [
        '\n',
        '复盘档案里后来多了一条注释：该用户曾三次投诉\u201c系统通知干扰睡眠\u201d。投诉被归类为\u201c非紧急反馈\u201d，未进入响应队列。\n',
    ]),
]

for after_line, new_lines in insertions:
    idx = after_line  # insert after this line (0-indexed: after_line is 1-indexed line number)
    lines[idx:idx] = new_lines
    label = new_lines[1].strip()[:30] if len(new_lines) > 1 else 'seed'
    print(f'  OK after L{after_line}: {label}...')

with open(MAIN, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Inserted {len(insertions)} foreshadowing seeds')
