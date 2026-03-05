
"""
报表生成系统
支持Excel、PDF、HTML格式的报表生成
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
from pathlib import Path


class ReportGenerator:
    """报表生成器核心类"""
    
    def __init__(self, title: str = "数据报表"):
        self.title = title
        self.data = None
        self.summary = {}
        self.charts = []
        
    def load_data(self, data: Any, source_type: str = "dataframe"):
        """加载数据源"""
        if source_type == "dataframe":
            self.data = data
        elif source_type == "dict":
            self.data = pd.DataFrame(data)
        elif source_type == "csv":
            self.data = pd.read_csv(data)
        elif source_type == "excel":
            self.data = pd.read_excel(data)
        elif source_type == "json":
            self.data = pd.read_json(data)
        else:
            raise ValueError(f"不支持的数据源类型: {source_type}")
        return self
    
    def add_summary(self, key: str, value: Any):
        """添加汇总信息"""
        self.summary[key] = value
        return self
    
    def calculate_statistics(self, columns: List[str] = None):
        """计算统计信息"""
        if self.data is None:
            raise ValueError("请先加载数据")
        
        if columns is None:
            columns = self.data.select_dtypes(include=['number']).columns.tolist()
        
        stats = {}
        for col in columns:
            if col in self.data.columns:
                stats[col] = {
                    '总计': self.data[col].sum(),
                    '平均值': self.data[col].mean(),
                    '最大值': self.data[col].max(),
                    '最小值': self.data[col].min(),
                    '中位数': self.data[col].median()
                }
        
        self.summary['统计信息'] = stats
        return self
    
    def add_chart_config(self, chart_type: str, x_column: str, y_column: str, 
                        title: str = ""):
        """添加图表配置"""
        self.charts.append({
            'type': chart_type,
            'x': x_column,
            'y': y_column,
            'title': title or f"{y_column} vs {x_column}"
        })
        return self
    
    def to_excel(self, output_path: str, sheet_name: str = "数据报表"):
        """导出为Excel格式"""
        if self.data is None:
            raise ValueError("没有数据可导出")
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 写入主数据
            self.data.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # 写入汇总信息
            if self.summary:
                summary_df = pd.DataFrame([self.summary])
                summary_df.to_excel(writer, sheet_name="汇总", index=False)
            
            # 如果有统计信息，单独写入
            if '统计信息' in self.summary:
                stats_df = pd.DataFrame(self.summary['统计信息']).T
                stats_df.to_excel(writer, sheet_name="统计分析")
        
        return output_path
    
    def to_html(self, output_path: str):
        """导出为HTML格式"""
        if self.data is None:
            raise ValueError("没有数据可导出")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .summary {{
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: #888;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{self.title}</h1>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        {self._generate_summary_html()}
        
        <h2>数据详情</h2>
        {self.data.to_html(index=False, classes='data-table')}
        
        <div class="footer">
            <p>报表由系统自动生成</p>
        </div>
    </div>
</body>
</html>
"""
        
        Path(output_path).write_text(html_content, encoding='utf-8')
        return output_path
    
    def _generate_summary_html(self) -> str:
        """生成汇总信息的HTML"""
        if not self.summary:
            return ""
        
        html = '<div class="summary"><h2>汇总信息</h2>'
        
        for key, value in self.summary.items():
            if key == '统计信息':
                html += '<h3>统计分析</h3>'
                stats_df = pd.DataFrame(value).T
                html += stats_df.to_html()
            else:
                html += f'<p><strong>{key}:</strong> {value}</p>'
        
        html += '</div>'
        return html
    
    def to_pdf(self, output_path: str):
        """导出为PDF格式（需要安装reportlab）"""
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
        except ImportError:
            raise ImportError("请安装reportlab: pip install reportlab")
        
        if self.data is None:
            raise ValueError("没有数据可导出")
        
        doc = SimpleDocTemplate(output_path, pagesize=landscape(A4))
        elements = []
        styles = getSampleStyleSheet()
        
        # 标题
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#333333'),
            spaceAfter=30,
        )
        elements.append(Paragraph(self.title, title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # 汇总信息
        if self.summary:
            elements.append(Paragraph("汇总信息", styles['Heading2']))
            for key, value in self.summary.items():
                if key != '统计信息':
                    elements.append(Paragraph(f"{key}: {value}", styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
        
        # 数据表格
        elements.append(Paragraph("数据详情", styles['Heading2']))
        
        # 转换数据为表格格式
        data_list = [self.data.columns.tolist()] + self.data.values.tolist()
        
        # 限制显示行数
        max_rows = 50
        if len(data_list) > max_rows:
            data_list = data_list[:max_rows]
            elements.append(Paragraph(f"注: 仅显示前{max_rows-1}行数据", styles['Normal']))
        
        table = Table(data_list)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        return output_path
    
    def to_json(self, output_path: str):
        """导出为JSON格式"""
        if self.data is None:
            raise ValueError("没有数据可导出")
        
        report_data = {
            'title': self.title,
            'generated_at': datetime.now().isoformat(),
            'summary': self.summary,
            'data': self.data.to_dict(orient='records')
        }
        
        Path(output_path).write_text(
            json.dumps(report_data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        
        return output_path


class DataAggregator:
    """数据聚合工具类"""
    
    @staticmethod
    def group_by_sum(df: pd.DataFrame, group_col: str, sum_cols: List[str]):
        """按列分组求和"""
        return df.groupby(group_col)[sum_cols].sum().reset_index()
    
    @staticmethod
    def group_by_count(df: pd.DataFrame, group_col: str):
        """按列分组计数"""
        return df.groupby(group_col).size().reset_index(name='count')
    
    @staticmethod
    def pivot_table(df: pd.DataFrame, index: str, columns: str, 
                   values: str, aggfunc: str = 'sum'):
        """创建数据透视表"""
        return pd.pivot_table(df, index=index, columns=columns, 
                            values=values, aggfunc=aggfunc)
    
    @staticmethod
    def time_series_resample(df: pd.DataFrame, date_col: str, 
                            freq: str = 'D', agg_dict: Dict = None):
        """时间序列重采样"""
        df[date_col] = pd.to_datetime(df[date_col])
        df.set_index(date_col, inplace=True)
        
        if agg_dict:
            return df.resample(freq).agg(agg_dict).reset_index()
        else:
            return df.resample(freq).sum().reset_index()


# 使用示例
if __name__ == "__main__":
    # 创建示例数据
    sample_data = {
        '日期': pd.date_range('2024-01-01', periods=10),
        '产品': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C'],
        '销售额': [1000, 1500, 1200, 800, 1600, 1100, 900, 1400, 1300, 950],
        '数量': [10, 15, 12, 8, 16, 11, 9, 14, 13, 10]
    }
    
    # 生成报表
    report = ReportGenerator(title="销售数据报表")
    report.load_data(sample_data, source_type="dict")
    report.add_summary("报表周期", "2024-01-01 至 2024-01-10")
    report.add_summary("总销售额", f"{sum(sample_data['销售额'])}元")
    report.calculate_statistics(['销售额', '数量'])
    
    # 导出多种格式
    report.to_excel("销售报表.xlsx")
    report.to_html("销售报表.html")
    report.to_json("销售报表.json")
    
    print("报表生成完成！")
