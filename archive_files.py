#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对比根目录和子目录文件，将有用内容吸收后归档
"""

import os
import shutil

def get_file_size(filepath):
    """获取文件大小（KB）"""
    return round(os.path.getsize(filepath) / 1024, 1)

def read_file(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        with open(filepath, 'r', encoding='gbk') as f:
            return f.read()

def main():
    base_dir = r"D:\_Progs\共振一元论"
    archive_dir = os.path.join(base_dir, "99-归档", "根目录原始文件")
    
    # 确保归档目录存在
    os.makedirs(archive_dir, exist_ok=True)
    
    # 定义文件映射关系
    file_mappings = {
        # MFO系列 - 旧体系，直接归档
        "MFO.101.本体论.互扰流显.md": None,
        "MFO.201.演化定律.互扰流显.md": None,
        "MFO.203.存在状态论.互扰流显.md": None,
        "MFO.205.规范跃迁动力机制.互扰流显.md": None,
        "MFO.301.意识问题.互扰流显.md": None,
        "MFO.303.感显扰动论.互扰流显.md": None,
        "MFO.305.价值层级论.互扰流显.md": None,
        "MFO.307.认识论基础.互扰流显.md": None,
        "MFO.401.四重展开.互扰流显.md": None,
        "MFO.501.核心叙事.互扰流显.md": None,
        "MFO.601.外部对话.互扰流显.md": None,
        "MFO.701.张力讨论.互扰流显.md": None,
        "MFO.801.社会冲击.互扰流显.md": None,
        "MFO_00_本体论推导_互扰流显.md": None,
        "MFO_SCI_001_科学形式化.md": None,
        "MFO_SCI_002_跨行业形式化概览.md": None,
        "MFO_SCI_003_高适配行业推导手册.md": None,
        "MFO_SCI_004_张力推导记录与修正建议.md": None,
        
        # RM系列 - 需要合并到对应子目录
        "RM.101.本体论.共振一元论.md": "10-哲学核心层（RM）/RM.P01.本体.世界由稳定结构构成.md",
        "RM.102.意识与感受.共振一元论.md": "10-哲学核心层（RM）/RM.P05.心灵.感受与意义.md",
        "RM.103.时空本体论.共振一元论.md": "10-哲学核心层（RM）/RM.P03.本体.暂稳态与可转换性.md",
        "RM.104.价值与能效原理.共振一元论.md": "10-哲学核心层（RM）/RM.P05b.心灵.价值与效价.md",
        "RM.201.演化定律.共振一元论.md": "30-文明演化层（ECET）/RM.ECET.演化定律.md",
        "RM.202.状态与规范.共振一元论.md": "30-文明演化层（ECET）/RM.ECET.状态与规范跃迁.md",
        "RM.301.感显扰动论.共振一元论.md": "10-哲学核心层（RM）/RM.P06.认识.认识的边界与感显扰动.md",
        "RM.302.认识论基础.共振一元论.md": "10-哲学核心层（RM）/RM.P07.认识.渐近线推断.md",
        "RM.401.文明与责任.共振一元论.md": "40-责任架构层（TAT）/RM.TAT.文明与责任.md",
        "RM.402.ECET.共振一元论.md": "30-文明演化层（ECET）/RM.ECET.理论基础.md",
        "RM.403.TAT.共振一元论.md": "40-责任架构层（TAT）/RM.TAT.责任架构理论.md",
        "RM.404.张力讨论.共振一元论.md": "10-哲学核心层（RM）/RM.P16.对话.与当代哲学张力.md",
        "RM.405.ODD.共振一元论.md": "50-工程方法层（ODD）/RM.ODD.工程方法论.md",
        "RM.体系跟踪主文件.md": "00-索引与导航/RM.体系跟踪主文件.md",
        "RM.理论定位申明.md": "00-索引与导航/RM.理论定位申明.md",
    }
    
    print("=== 开始处理文件 ===\n")
    
    # 处理MFO文件（直接归档）
    print("【MFO系列 - 直接归档】")
    for filename in file_mappings:
        if filename.startswith("MFO"):
            src_path = os.path.join(base_dir, filename)
            if os.path.exists(src_path):
                dst_path = os.path.join(archive_dir, filename)
                shutil.move(src_path, dst_path)
                size = get_file_size(dst_path)
                print(f"  ✓ 归档: {filename} ({size}KB)")
    
    print("\n【RM系列 - 对比并归档】")
    for root_file, target_file in file_mappings.items():
        if root_file.startswith("RM") and target_file:
            root_path = os.path.join(base_dir, root_file)
            target_path = os.path.join(base_dir, target_file)
            
            if not os.path.exists(root_path):
                print(f"  ⚠ 跳过（不存在）: {root_file}")
                continue
            
            if os.path.exists(target_path):
                root_size = get_file_size(root_path)
                target_size = get_file_size(target_path)
                print(f"  📄 {root_file}")
                print(f"     根目录: {root_size}KB | 子目录: {target_size}KB")
                
                # 如果根目录文件更大，可能需要合并
                if root_size > target_size:
                    print(f"     ⚠ 根目录版本更大，可能需要手动检查")
            else:
                print(f"  ⚠ 子目录文件不存在: {target_file}")
            
            # 归档根目录文件
            dst_path = os.path.join(archive_dir, root_file)
            shutil.move(root_path, dst_path)
            print(f"     ✓ 已归档")
    
    print("\n=== 处理完成 ===")
    print(f"归档位置: {archive_dir}")

if __name__ == "__main__":
    main()
