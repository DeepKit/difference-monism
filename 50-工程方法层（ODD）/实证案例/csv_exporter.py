
import csv
import io
from typing import List, Dict, Any, Optional, Union
from pathlib import Path


class CSVExporter:
    def __init__(
        self,
        columns: Optional[List[str]] = None,
        encoding: str = 'utf-8',
        null_value: str = '',
        delimiter: str = ',',
        quotechar: str = '"',
        include_header: bool = True,
        newline: str = ''
    ):
        self.columns = columns
        self.encoding = encoding
        self.null_value = null_value
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.include_header = include_header
        self.newline = newline

    def _process_value(self, value: Any) -> str:
        if value is None or (isinstance(value, float) and str(value) == 'nan'):
            return self.null_value
        return str(value)

    def _get_columns(self, data: List[Dict[str, Any]]) -> List[str]:
        if self.columns:
            return self.columns
        if data:
            return list(data[0].keys())
        return []

    def export_to_file(
        self,
        data: List[Dict[str, Any]],
        filepath: Union[str, Path],
        mode: str = 'w'
    ) -> None:
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, mode, encoding=self.encoding, newline=self.newline) as f:
            self._write_csv(f, data)

    def export_to_string(self, data: List[Dict[str, Any]]) -> str:
        output = io.StringIO()
        self._write_csv(output, data)
        return output.getvalue()

    def export_to_bytes(self, data: List[Dict[str, Any]]) -> bytes:
        csv_string = self.export_to_string(data)
        return csv_string.encode(self.encoding)

    def _write_csv(self, file_obj, data: List[Dict[str, Any]]) -> None:
        if not data:
            return

        columns = self._get_columns(data)
        
        writer = csv.DictWriter(
            file_obj,
            fieldnames=columns,
            delimiter=self.delimiter,
            quotechar=self.quotechar,
            quoting=csv.QUOTE_MINIMAL,
            extrasaction='ignore'
        )

        if self.include_header:
            writer.writeheader()

        for row in data:
            processed_row = {
                col: self._process_value(row.get(col))
                for col in columns
            }
            writer.writerow(processed_row)

    def append_to_file(
        self,
        data: List[Dict[str, Any]],
        filepath: Union[str, Path]
    ) -> None:
        filepath = Path(filepath)
        file_exists = filepath.exists()
        
        with open(filepath, 'a', encoding=self.encoding, newline=self.newline) as f:
            if not file_exists and self.include_header:
                self._write_csv(f, data)
            else:
                original_header = self.include_header
                self.include_header = False
                self._write_csv(f, data)
                self.include_header = original_header


# 使用示例
if __name__ == '__main__':
    # 示例数据
    data = [
        {'name': '张三', 'age': 25, 'city': '北京', 'salary': None},
        {'name': '李四', 'age': None, 'city': '上海', 'salary': 8000},
        {'name': '王五', 'age': 35, 'city': None, 'salary': 12000},
    ]

    # 基本导出
    exporter = CSVExporter(encoding='utf-8', null_value='N/A')
    exporter.export_to_file(data, 'output.csv')

    # 自定义列顺序
    exporter_custom = CSVExporter(
        columns=['name', 'city', 'age'],
        encoding='utf-8-sig',  # Excel兼容
        null_value='--'
    )
    exporter_custom.export_to_file(data, 'output_custom.csv')

    # 导出为字符串
    csv_string = exporter.export_to_string(data)
    print(csv_string)

    # 追加数据
    new_data = [{'name': '赵六', 'age': 28, 'city': '深圳', 'salary': 15000}]
    exporter.append_to_file(new_data, 'output.csv')
