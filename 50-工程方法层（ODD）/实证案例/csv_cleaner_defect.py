import pandas as pd
from typing import Optional, List


class CSVCleaner:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = pd.read_csv(filepath)
        self.original_shape = self.df.shape
    
    def remove_duplicates(self, subset: Optional[List[str]] = None):
        """删除重复行"""
        self.df = self.df.drop_duplicates(subset=subset)
        return self
    
    def remove_empty_rows(self):
        """删除空行"""
        self.df = self.df.dropna(how='all')
        return self
    
    def remove_empty_columns(self):
        """删除空列"""
        self.df = self.df.dropna(axis=1, how='all')
        return self
    
    def fill_missing(self, method='ffill', columns: Optional[List[str]] = None):
        """填充缺失值 (ffill/bfill/mean/median/mode)"""
        cols = columns or self.df.columns
        if method in ['ffill', 'bfill']:
            self.df[cols] = self.df[cols].fillna(method=method)
        elif method == 'mean':
            self.df[cols] = self.df[cols].fillna(self.df[cols].mean())
        elif method == 'median':
            self.df[cols] = self.df[cols].fillna(self.df[cols].median())
        elif method == 'mode':
            self.df[cols] = self.df[cols].fillna(self.df[cols].mode().iloc[0])
        return self
    
    def strip_whitespace(self):
        """去除字符串列的首尾空格"""
        str_cols = self.df.select_dtypes(include=['object']).columns
        self.df[str_cols] = self.df[str_cols].apply(lambda x: x.str.strip())
        return self
    
    def drop_columns(self, columns: List[str]):
        """删除指定列"""
        self.df = self.df.drop(columns=columns, errors='ignore')
        return self
    
    def rename_columns(self, mapping: dict):
        """重命名列"""
        self.df = self.df.rename(columns=mapping)
        return self
    
    def save(self, output_path: str, index=False):
        """保存清洗后的数据"""
        self.df.to_csv(output_path, index=index)
        print(f"已保存到 {output_path}")
        print(f"原始数据: {self.original_shape}, 清洗后: {self.df.shape}")
        return self
    
    def get_dataframe(self):
        """获取清洗后的DataFrame"""
        return self.df


# 使用示例
if __name__ == "__main__":
    cleaner = CSVCleaner('data.csv')
    cleaner.remove_duplicates() \
           .remove_empty_rows() \
           .strip_whitespace() \
           .fill_missing(method='ffill') \
           .save('cleaned_data.csv')