import csv
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class ReportGenerator:
    """报表生成器类"""
    
    def __init__(self, title: str = "Report", author: str = "System"):
        self.title = title
        self.author = author
        self.data: List[Dict[str, Any]] = []
        self.headers: List[str] = []
        self.created_at = datetime.now()
    
    def set_data(self, data: List[Dict[str, Any]], headers: Optional[List[str]] = None):
        """设置报表数据"""
        self.data = data
        if headers:
            self.headers = headers
        elif data:
            self.headers = list(data[0].keys())
    
    def add_row(self, row: Dict[str, Any]):
        """添加单行数据"""
        self.data.append(row)
        if not self.headers and row:
            self.headers = list(row.keys())
    
    def to_csv(self, filepath: str):
        """导出为CSV格式"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.data)
    
    def to_json(self, filepath: str, indent: int = 2):
        """导出为JSON格式"""
        report = {
            'title': self.title,
            'author': self.author,
            'created_at': self.created_at.isoformat(),
            'data': self.data
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=indent, ensure_ascii=False)
    
    def to_html(self, filepath: str):
        """导出为HTML格式"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .meta {{ color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>{self.title}</h1>
    <p class="meta">作者: {self.author} | 生成时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <table>
        <thead>
            <tr>
                {''.join(f'<th>{h}</th>' for h in self.headers)}
            </tr>
        </thead>
        <tbody>
"""
        for row in self.data:
            html += "            <tr>\n"
            for header in self.headers:
                html += f"                <td>{row.get(header, '')}</td>\n"
            html += "            </tr>\n"
        
        html += """        </tbody>
    </table>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def to_txt(self, filepath: str):
        """导出为纯文本格式"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{self.title}\n")
            f.write(f"{'=' * len(self.title)}\n\n")
            f.write(f"作者: {self.author}\n")
            f.write(f"生成时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if not self.data:
                f.write("无数据\n")
                return
            
            col_widths = {h: len(h) for h in self.headers}
            for row in self.data:
                for header in self.headers:
                    col_widths[header] = max(col_widths[header], len(str(row.get(header, ''))))
            
            header_line = " | ".join(h.ljust(col_widths[h]) for h in self.headers)
            f.write(header_line + "\n")
            f.write("-" * len(header_line) + "\n")
            
            for row in self.data:
                row_line = " | ".join(str(row.get(h, '')).ljust(col_widths[h]) for h in self.headers)
                f.write(row_line + "\n")
    
    def get_summary(self) -> Dict[str, Any]:
        """获取报表摘要信息"""
        return {
            'title': self.title,
            'author': self.author,
            'created_at': self.created_at.isoformat(),
            'row_count': len(self.data),
            'column_count': len(self.headers),
            'headers': self.headers
        }


# 使用示例
if __name__ == "__main__":
    # 创建报表生成器
    report = ReportGenerator(title="销售报表", author="张三")
    
    # 添加数据
    data = [
        {'日期': '2024-01-01', '产品': 'A', '销量': 100, '金额': 5000},
        {'日期': '2024-01-02', '产品': 'B', '销量': 150, '金额': 7500},
        {'日期': '2024-01-03', '产品': 'C', '销量': 200, '金额': 10000},
    ]
    report.set_data(data)
    
    # 导出不同格式
    report.to_csv('report.csv')
    report.to_json('report.json')
    report.to_html('report.html')
    report.to_txt('report.txt')
    
    # 获取摘要
    print(report.get_summary())