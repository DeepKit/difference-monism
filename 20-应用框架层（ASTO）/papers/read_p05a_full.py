# -*- coding: utf-8 -*-
import glob, os, sys
sys.stdout = open(r'D:\_Progs\01Center\ASTO\papers\read_p05a_full.txt', 'w', encoding='utf-8')
base = r'D:\_Progs\01Center\ASTO\papers'
for name in ['ASTO.P05a', 'ASTO.P06', 'ASTO.P07', 'ASTO.P08']:
    m = glob.glob(os.path.join(base, name + '*.md'))
    if m:
        print(f'\n\n========== {name} | {os.path.basename(m[0])} ==========\n')
        print(open(m[0], encoding='utf-8').read())
    else:
        print(f'[NOT FOUND] {name}')
