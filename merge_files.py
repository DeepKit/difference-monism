#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并P系列文件到RM.P系列，保持UTF-8编码
"""

import os
import sys

def read_file(filepath):
    """以UTF-8读取文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """以UTF-8写入文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def merge_files(p_file, rm_p_file, output_file, separator="\n\n---\n\n"):
    """合并两个文件"""
    try:
        content_p = read_file(p_file)
        content_rm_p = read_file(rm_p_file)
        
        merged = content_p + separator + content_rm_p
        write_file(output_file, merged)
        
        print(f"✓ 合并完成: {output_file}")
        return True
    except Exception as e:
        print(f"✗ 错误: {e}")
        return False

def main():
    base_dir = r"D:\_Progs\共振一元论\10-哲学核心层（RM）"
    os.chdir(base_dir)
    
    # 定义合并规则
    merges = [
        # (P文件, RM.P文件, 输出文件, 分隔符标题)
        ("P01.本体.世界由稳定结构构成.md", "RM.P01.本体.世界由稳定结构构成.md", 
         "RM.P01.本体.世界由稳定结构构成.md", "\n\n---\n\n# 详细推导\n\n"),
        
        ("P03.本体.暂稳态与可转换性.md", "RM.P03.本体.暂稳态与时空.md",
         "RM.P03.本体.暂稳态与可转换性.md", "\n\n---\n\n# 时空推导\n\n"),
        
        ("P04.心灵.意识的结构.md", "RM.P04.心灵.硬问题的完整推导.md",
         "RM.P04.心灵.意识的结构与硬问题推导.md", "\n\n---\n\n# 附录：硬问题的完整推导\n\n"),
        
        ("P05.心灵.感受与意义.md", "RM.P05.心灵.感受与意义完整版.md",
         "RM.P05.心灵.感受与意义.md", "\n\n---\n\n# 完整推导\n\n"),
        
        ("P06.认识.认识的边界.md", "RM.P06.认识.感显扰动论.md",
         "RM.P06.认识.认识的边界与感显扰动.md", "\n\n---\n\n# 感显扰动论\n\n"),
        
        ("P07.认识.渐近线推断.md", "RM.P07.认识.渐近线推断完整版.md",
         "RM.P07.认识.渐近线推断.md", "\n\n---\n\n# 详细推导\n\n"),
    ]
    
    # 执行合并
    for p_file, rm_p_file, output, separator in merges:
        if os.path.exists(p_file) and os.path.exists(rm_p_file):
            if merge_files(p_file, rm_p_file, output, separator):
                # 删除源文件
                os.remove(p_file)
                if rm_p_file != output:
                    os.remove(rm_p_file)
                print(f"  已删除源文件: {p_file}, {rm_p_file}")
        else:
            print(f"⚠ 跳过（文件不存在）: {p_file} 或 {rm_p_file}")
    
    # 重命名剩余的文件
    renames = [
        ("P02.本体.共扰结构与涌现.md", "RM.P02.本体.共扰结构与涌现.md"),
        ("P08.伦理.责任的拓扑.md", "RM.P08.伦理.责任的拓扑.md"),
        ("P09.政治.文明的韧性.md", "RM.P09.政治.文明的韧性.md"),
        ("P10.政治.演化与约束.md", "RM.P10.政治.演化与约束.md"),
        ("P11.对话.与结构实在论.md", "RM.P11.对话.与结构实在论.md"),
        ("P12.对话.与过程哲学.md", "RM.P12.对话.与过程哲学.md"),
        ("P13.对话.与现象学.md", "RM.P13.对话.与现象学.md"),
        ("P14.对话.与佛学缘起论.md", "RM.P14.对话.与佛学缘起论.md"),
        ("P15.对话.开放边界与诚实.md", "RM.P15.对话.开放边界与诚实.md"),
    ]
    
    for old_name, new_name in renames:
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            print(f"✓ 重命名: {old_name} → {new_name}")
        else:
            print(f"⚠ 跳过（文件不存在）: {old_name}")
    
    print("\n完成！")

if __name__ == "__main__":
    main()
