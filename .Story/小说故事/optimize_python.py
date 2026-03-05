#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASTO八部曲优化脚本
基于TAT优化建议-v2.md
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

class NovelOptimizer:
    def __init__(self, book_path):
        self.book_path = Path(book_path)
        self.results = []
        
        # 优化规则
        self.rules = [
            {
                "name": "去除'突然'",
                "pattern": r'突然',
                "replacement": '',
                "should_fix": True,
                "description": "全书=0，用动作触发替代"
            },
            {
                "name": "作者裁判句",
                "patterns": [r'他觉得', r'她意识到', r'仿佛', r'似乎', r'好像', r'感觉', r'意识到', r'认识到'],
                "replacement": '',
                "should_fix": True,
                "description": "改为可观察的身体动作或环境变化"
            },
            {
                "name": "概念注释", 
                "patterns": [r'这意味着', r'其实', r'说穿了', r'换句话说', r'换言之', r'也就是说', r'本质上'],
                "replacement": '',
                "should_fix": True,
                "description": "删除，用场景自证"
            },
            {
                "name": "象征标注",
                "patterns": [r'象征着', r'暗示了', r'这就是所谓的', r'代表了', r'意味着'],
                "replacement": '',
                "should_fix": True,
                "description": "删除，信任读者"
            },
            {
                "name": "统计'看着/望着'",
                "pattern": r'看着|望着',
                "replacement": '',  # 只统计，不自动替换
                "should_fix": False,
                "description": "每万字不超过3次"
            },
            {
                "name": "TAT术语检查",
                "patterns": [
                    r'责任锚定', r'物质吸收能力', r'五态', r'六阶', r'七序', 
                    r'剩馀物', r'穿透式追责', r'调节延迟', r'熔断', 
                    r'随机公民陪审团', r'双重钥匙', r'痛苦私有性'
                ],
                "replacement": '',
                "should_fix": True,
                "description": "正文中应为0"
            }
        ]
        
        # 情绪形容词（需要手动处理）
        self.emotion_patterns = [
            r'他感到一阵', r'她感到一阵', r'深深地', r'无比地'
        ]
    
    def find_chapter_files(self):
        """查找章节文件"""
        chapter_files = []
        exclude_keywords = [
            '产出物', '指南', '大纲', '优化', 'AGENTS', 'better', 'readme',
            '任务', '清单', '分析', '报告', '白皮书', '批判', '宣言', '计划'
        ]
        
        # 特殊处理的小说
        special_books = {
            '《验收之前》': ['验收之前-正文-卷一.md', '验收之前-正文-卷二.md', 
                          '验收之前-正文-卷三.md', '验收之前-正文-卷四.md'],
            '《宇宙之光》': ['宇宙之光_全书.md']
        }
        
        book_name = self.book_path.name
        
        # 如果是特殊处理的小说
        if book_name in special_books:
            for filename in special_books[book_name]:
                file_path = self.book_path / filename
                if file_path.exists():
                    chapter_files.append(file_path)
            return chapter_files
        
        # 通用查找逻辑
        for file_path in self.book_path.rglob('*.md'):
            filename = file_path.name
            
            # 检查是否章节文件
            is_chapter = (
                re.search(r'第[0-9一二三四五六七八九十]+章', filename) or
                re.search(r'^[0-9]+_', filename) or
                re.search(r'^[一二三四五六七八九十]+、', filename) or
                re.search(r'^[0-9]+_', filename) or
                re.search(r'^第[0-9]+章', filename)
            )
            
            # 排除非章节文件
            is_excluded = any(keyword in filename for keyword in exclude_keywords)
            
            if is_chapter and not is_excluded:
                chapter_files.append(file_path)
        
        return chapter_files
    
    def analyze_file(self, file_path, fix_problems=False):
        """分析单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except:
                print(f"  错误: 无法读取文件 {file_path}")
                return None
        
        file_result = {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'original_size': len(content),
            'word_count': len(content.split()),
            'issues': [],
            'changes': [],
            'optimized_content': content
        }
        
        current_content = content
        
        # 应用优化规则
        for rule in self.rules:
            if 'pattern' in rule:
                # 单模式规则
                pattern = rule['pattern']
                matches = re.findall(pattern, current_content)
                
                if matches:
                    count = len(matches)
                    file_result['issues'].append(f"{rule['name']}: {count}处")
                    
                    if rule['should_fix'] and fix_problems:
                        new_content = re.sub(pattern, rule['replacement'], current_content)
                        if new_content != current_content:
                            file_result['changes'].append(f"修复了{rule['name']}: {count}处")
                            current_content = new_content
                            
            elif 'patterns' in rule:
                # 多模式规则
                for pattern in rule['patterns']:
                    matches = re.findall(pattern, current_content)
                    
                    if matches:
                        count = len(matches)
                        file_result['issues'].append(f"{rule['name']} - '{pattern}': {count}处")
                        
                        if rule['should_fix'] and fix_problems:
                            new_content = re.sub(pattern, rule['replacement'], current_content)
                            if new_content != current_content:
                                file_result['changes'].append(f"修复了{rule['name']} - '{pattern}': {count}处")
                                current_content = new_content
        
        # 检查情绪形容词
        for pattern in self.emotion_patterns:
            matches = re.findall(pattern, current_content)
            if matches:
                count = len(matches)
                file_result['issues'].append(f"情绪形容词 '{pattern}': {count}处（建议改为具体生理反应）")
        
        file_result['optimized_content'] = current_content
        
        return file_result
    
    def run_analysis(self, fix_problems=False, create_backup=False):
        """运行分析"""
        print(f"=== ASTO小说优化工具 ===")
        print(f"目标路径: {self.book_path}")
        print(f"模式: {'修复模式' if fix_problems else '分析模式'}")
        print()
        
        # 查找章节文件
        chapter_files = self.find_chapter_files()
        print(f"找到 {len(chapter_files)} 个章节文件")
        print()
        
        # 创建备份
        if create_backup:
            backup_dir = self.book_path / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_dir.mkdir(parents=True, exist_ok=True)
            print(f"创建备份到: {backup_dir}")
            
            for file_path in chapter_files:
                relative_path = file_path.relative_to(self.book_path)
                backup_file = backup_dir / relative_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'rb') as src, open(backup_file, 'wb') as dst:
                    dst.write(src.read())
            print()
        
        # 分析文件
        files_with_issues = 0
        files_optimized = 0
        
        for file_path in chapter_files:
            print(f"处理: {file_path.name}", end='')
            
            result = self.analyze_file(file_path, fix_problems)
            if result is None:
                print(" [错误]")
                continue
            
            self.results.append(result)
            
            if result['issues']:
                files_with_issues += 1
                print(f" [发现{len(result['issues'])}类问题]")
            else:
                print(" [无问题]")
            
            # 保存优化版本
            if result['changes'] and fix_problems:
                optimized_file = file_path.parent / f"{file_path.stem}_v3.md"
                try:
                    with open(optimized_file, 'w', encoding='utf-8') as f:
                        f.write(result['optimized_content'])
                    print(f"   -> 创建优化版本: {optimized_file.name}")
                    files_optimized += 1
                except Exception as e:
                    print(f"   -> 保存失败: {e}")
        
        # 生成报告
        self.generate_report(files_with_issues, files_optimized, len(chapter_files))
        
        return self.results
    
    def generate_report(self, files_with_issues, files_optimized, total_files):
        """生成优化报告"""
        print()
        print("=== 优化报告 ===")
        print(f"总文件数: {total_files}")
        print(f"存在问题文件: {files_with_issues}")
        print(f"已优化文件: {files_optimized}")
        print()
        
        # 统计问题类型
        issue_stats = {}
        for result in self.results:
            for issue in result['issues']:
                issue_type = issue.split(':')[0]
                issue_stats[issue_type] = issue_stats.get(issue_type, 0) + 1
        
        if issue_stats:
            print("问题类型分布:")
            for issue_type, count in sorted(issue_stats.items()):
                print(f"  {issue_type}: {count}个文件存在")
            print()
        
        # 详细报告
        report_path = self.book_path / "optimization_report.txt"
        report_content = [
            "ASTO小说优化报告",
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"目标路径: {self.book_path}",
            f"文件数量: {total_files}",
            f"存在问题文件: {files_with_issues}",
            f"已优化文件: {files_optimized}",
            "",
            "== 问题统计 ==",
            ""
        ]
        
        if issue_stats:
            report_content.append("问题类型分布:")
            for issue_type, count in sorted(issue_stats.items()):
                report_content.append(f"  {issue_type}: {count}个文件存在")
            report_content.append("")
        
        report_content.append("== 详细文件分析 ==")
        report_content.append("")
        
        for result in self.results:
            if result['issues']:
                report_content.append(f"文件: {result['file_name']}")
                report_content.append(f"字数: {result['word_count']}")
                report_content.append("问题:")
                for issue in result['issues']:
                    report_content.append(f"  - {issue}")
                
                if result['changes']:
                    report_content.append("修复:")
                    for change in result['changes']:
                        report_content.append(f"  - {change}")
                
                report_content.append("")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_content))
            print(f"报告已保存到: {report_path}")
        except Exception as e:
            print(f"保存报告失败: {e}")
        
        print()
        print("=== 下一步建议 ===")
        print("1. 查看详细报告")
        print("2. 手动处理复杂问题（情绪形容词、象征意义等）")
        print("3. 检查每章的'问题钉子'和'动作钉子'")
        print("4. 为关键人物添加'反向欲望'")
        print("5. 确保符合各卷情绪梯度")

def main():
    parser = argparse.ArgumentParser(description='ASTO八部曲优化工具')
    parser.add_argument('book_path', help='小说目录路径')
    parser.add_argument('--analyze', action='store_true', help='仅分析模式')
    parser.add_argument('--fix', action='store_true', help='修复简单问题')
    parser.add_argument('--backup', action='store_true', help='创建备份')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.book_path):
        print(f"错误: 路径不存在 {args.book_path}")
        sys.exit(1)
    
    optimizer = NovelOptimizer(args.book_path)
    fix_problems = args.fix and not args.analyze
    optimizer.run_analysis(fix_problems=fix_problems, create_backup=args.backup)

if __name__ == '__main__':
    main()