#!/usr/bin/env python3
"""Fix name errors: P0-1 (沈工→许工 for 许冬) and P0-2 (周女士→孙女士)."""

import os

BASE = r"D:\_Progs\01Center\ASTO\小说故事\《凛冬之宪》\2.0"
MAIN = os.path.join(BASE, "ASTO.凛冬之宪--艰难的前进历程.md")
CH22_FILE = os.path.join(BASE, "第22章_未完成清单-产出物.md")

def fix_main():
    with open(MAIN, 'r', encoding='utf-8-sig') as f:
        text = f.read()
    
    changes = []
    
    # P0-1: Fix "沈工" when addressing 许冬 in Ch17
    # These are the ONLY two instances where 沈工 refers to 许冬 (not 沈知行)
    # L4260: K主任's message to 许冬
    old1 = '"沈工，ASTO 保护着十四亿个节点。'
    new1 = '"许工，ASTO 保护着十四亿个节点。'
    if old1 in text:
        text = text.replace(old1, new1, 1)
        changes.append("L4260: 沈工→许工 (K主任 message to 许冬)")
    
    # L4365: 实习生小张 to 许冬
    old2 = '"沈工，K主任说那个'
    new2 = '"许工，K主任说那个'
    if old2 in text:
        text = text.replace(old2, new2, 1)
        changes.append("L4365: 沈工→许工 (实习生 to 许冬)")
    
    # P0-2: Fix "周女士" → "孙女士" in Ch18
    count = text.count('周女士')
    text = text.replace('周女士', '孙女士')
    if count > 0:
        changes.append(f"周女士→孙女士: {count} instances")
    
    with open(MAIN, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return changes

def fix_ch22():
    with open(CH22_FILE, 'r', encoding='utf-8-sig') as f:
        text = f.read()
    
    changes = []
    if '沈许冬' in text:
        text = text.replace('沈许冬', '许冬')
        changes.append("Ch22产出物: 沈许冬→许冬")
        with open(CH22_FILE, 'w', encoding='utf-8') as f:
            f.write(text)
    
    return changes

if __name__ == '__main__':
    print("=== P0-1 + P0-2: Name fixes ===")
    c1 = fix_main()
    c2 = fix_ch22()
    for c in c1 + c2:
        print(f"  ✓ {c}")
    print(f"\nDone. {len(c1)+len(c2)} changes applied.")
