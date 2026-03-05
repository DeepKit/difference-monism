
import csv
from typing import List, Dict, Any, Union, Optional
from pathlib import Path


class CSVExporter:
    """CSV文件导出工具类"""
    
    def __init__(
        self,
        filepath: Union[str, Path],
        encoding: str = 'utf-8-sig',
        delimiter: str = ',',
        quoting: int = csv.QUOTE_MINIMAL
    ):
        """
        初始化CSV导出器
        
        Args:
            filepath: 导出文件路径
            encoding: 文件编码，默认utf-8-sig（兼容Excel）
            delimiter: 分隔符，默认逗号
            quoting: 引号策略
        """
        self.filepath = Path(filepath)
        self.encoding = encoding
        self.delimiter = delimiter
        self.quoting = quoting
    
    def export_from_dicts(
        self,
        data: List[Dict[str, Any]],
        fieldnames: Optional[List[str]] = None,
        include_header: bool = True
    ) -> None:
        """
        从字典列表导出CSV
        
        Args:
            data: 字典列表数据
            fieldnames: 字段名列表，None则使用第一条数据的键
            include_header: 是否包含表头
        """
        if not data:
            raise ValueError("数据不能为空")
        
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.filepath, 'w', newline='', encoding=self.encoding) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames,
                delimiter=self.delimiter,
                quoting=self.quoting
            )
            
            if include_header:
                writer.writeheader()
            
            writer.writerows(data)
    
    def export_from_lists(
        self,
        data: List[List[Any]],
        header: Optional[List[str]] = None
    ) -> None:
        """
        从列表导出CSV
        
        Args:
            data: 二维列表数据
            header: 表头列表
        """
        if not data:
            raise ValueError("数据不能为空")
        
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.filepath, 'w', newline='', encoding=self.encoding) as f:
            writer = csv.writer(
                f,
                delimiter=self.delimiter,
                quoting=self.quoting
            )
            
            if header:
                writer.writerow(header)
            
            writer.writerows(data)
    
    def append_rows(self, rows: List[Union[Dict, List]]) -> None:
        """
        追加行到现有CSV文件
        
        Args:
            rows: 要追加的行数据
        """
        if not rows:
            return
        
        mode = 'a' if self.filepath.exists() else 'w'
        
        with open(self.filepath, mode, newline='', encoding=self.encoding) as f:
            if isinstance(rows[0], dict):
                fieldnames = list(rows[0].keys())
                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames,
                    delimiter=self.delimiter,
                    quoting=self.quoting
                )
                if mode == 'w':
                    writer.writeheader()
                writer.writerows(rows)
            else:
                writer = csv.writer(
                    f,
                    delimiter=self.delimiter,
                    quoting=self.quoting
                )
                writer.writerows(rows)


def quick_export(
    filepath: Union[str, Path],
    data: Union[List[Dict], List[List]],
    **kwargs
) -> None:
    """
    快速导出CSV的便捷函数
    
    Args:
        filepath: 导出文件路径
        data: 数据（字典列表或二维列表）
        **kwargs: 其他参数传递给CSVExporter
    """
    exporter = CSVExporter(filepath, **kwargs)
    
    if data and isinstance(data[0], dict):
        exporter.export_from_dicts(data)
    else:
        exporter.export_from_lists(data)


# 使用示例
if __name__ == '__main__':
    # 示例1：从字典列表导出
    data_dicts = [
        {'姓名': '张三', '年龄': 25, '城市': '北京'},
        {'姓名': '李四', '年龄': 30, '城市': '上海'},
        {'姓名': '王五', '年龄': 28, '城市': '广州'}
    ]
    
    exporter = CSVExporter('output/users.csv')
    exporter.export_from_dicts(data_dicts)
    
    # 示例2：从列表导出
    data_lists = [
        ['张三', 25, '北京'],
        ['李四', 30, '上海'],
        ['王五', 28, '广州']
    ]
    
    exporter2 = CSVExporter('output/users2.csv')
    exporter2.export_from_lists(data_lists, header=['姓名', '年龄', '城市'])
    
    # 示例3：快速导出
    quick_export('output/quick.csv', data_dicts)
    
    # 示例4：追加数据
    new_data = [{'姓名': '赵六', '年龄': 35, '城市': '深圳'}]
    exporter.append_rows(new_data)
