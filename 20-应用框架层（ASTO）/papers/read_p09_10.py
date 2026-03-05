# -*- coding: utf-8 -*-
import glob, os, sys
sys.stdout = open(r'D:\_Progs\01Center\ASTO\papers\read_p09_10.txt', 'w', encoding='utf-8')
base = r'D:\_Progs\01Center\ASTO\papers'
for name in ['ASTO.P09a', 'ASTO.P09b', 'ASTO.P10', 'ASTO.P11', 'ASTO.P12', 'ASTO.P13']:
    m = glob.glob(os.path.join(base, name + '*.md'))
    if not m:
        m = glob.glob(os.path.join(base, '**', name + '*.md'), recursive=True)
    if m:
        print(f'\n\n========== {name} | {os.path.basename(m[0])} ==========\n')
        print(open(m[0], encoding='utf-8').read())
    else:
        print(f'[NOT FOUND] {name}')
