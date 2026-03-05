import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union, Callable
from pathlib import Path
import logging


class CSVCleaner:
    def __init__(self, filepath: str, encoding: str = 'utf-8'):
        self.filepath = Path(filepath)
        self.encoding = encoding
        self.df: Optional[pd.DataFrame] = None
        self.original_df: Optional[pd.DataFrame] = None
        self.logger = logging.getLogger(__name__)
        
    def load(self, **kwargs) -> 'CSVCleaner':
        try:
            self.df = pd.read_csv(self.filepath, encoding=self.encoding, **kwargs)
            self.original_df = self.df.copy()
            self.logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            return self
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")
    
    def reset(self) -> 'CSVCleaner':
        if self.original_df is not None:
            self.df = self.original_df.copy()
        return self
    
    def remove_duplicates(self, subset: Optional[List[str]] = None, keep: str = 'first') -> 'CSVCleaner':
        try:
            before = len(self.df)
            self.df = self.df.drop_duplicates(subset=subset, keep=keep)
            after = len(self.df)
            self.logger.info(f"Removed {before - after} duplicate rows")
            return self
        except Exception as e:
            raise Exception(f"Error removing duplicates: {str(e)}")
    
    def handle_missing(self, strategy: str = 'drop', columns: Optional[List[str]] = None, 
                      fill_value: Optional[Union[str, int, float, Dict]] = None) -> 'CSVCleaner':
        try:
            cols = columns or self.df.columns.tolist()
            
            if strategy == 'drop':
                self.df = self.df.dropna(subset=cols)
            elif strategy == 'fill':
                if fill_value is None:
                    raise ValueError("fill_value required for 'fill' strategy")
                self.df[cols] = self.df[cols].fillna(fill_value)
            elif strategy == 'forward':
                self.df[cols] = self.df[cols].fillna(method='ffill')
            elif strategy == 'backward':
                self.df[cols] = self.df[cols].fillna(method='bfill')
            elif strategy == 'mean':
                for col in cols:
                    if pd.api.types.is_numeric_dtype(self.df[col]):
                        self.df[col] = self.df[col].fillna(self.df[col].mean())
            elif strategy == 'median':
                for col in cols:
                    if pd.api.types.is_numeric_dtype(self.df[col]):
                        self.df[col] = self.df[col].fillna(self.df[col].median())
            elif strategy == 'mode':
                for col in cols:
                    mode_val = self.df[col].mode()
                    if len(mode_val) > 0:
                        self.df[col] = self.df[col].fillna(mode_val[0])
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
            
            return self
        except Exception as e:
            raise Exception(f"Error handling missing values: {str(e)}")
    
    def convert_types(self, type_map: Dict[str, str]) -> 'CSVCleaner':
        try:
            for col, dtype in type_map.items():
                if col not in self.df.columns:
                    raise ValueError(f"Column '{col}' not found")
                
                if dtype == 'datetime':
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                elif dtype == 'category':
                    self.df[col] = self.df[col].astype('category')
                else:
                    self.df[col] = self.df[col].astype(dtype)
            
            return self
        except Exception as e:
            raise Exception(f"Error converting types: {str(e)}")
    
    def remove_outliers(self, columns: List[str], method: str = 'iqr', threshold: float = 1.5) -> 'CSVCleaner':
        try:
            for col in columns:
                if col not in self.df.columns:
                    raise ValueError(f"Column '{col}' not found")
                
                if not pd.api.types.is_numeric_dtype(self.df[col]):
                    continue
                
                if method == 'iqr':
                    Q1 = self.df[col].quantile(0.25)
                    Q3 = self.df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - threshold * IQR
                    upper = Q3 + threshold * IQR
                    self.df = self.df[(self.df[col] >= lower) & (self.df[col] <= upper)]
                elif method == 'zscore':
                    z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                    self.df = self.df[z_scores < threshold]
                else:
                    raise ValueError(f"Unknown method: {method}")
            
            return self
        except Exception as e:
            raise Exception(f"Error removing outliers: {str(e)}")
    
    def drop_columns(self, columns: List[str]) -> 'CSVCleaner':
        try:
            self.df = self.df.drop(columns=columns, errors='ignore')
            return self
        except Exception as e:
            raise Exception(f"Error dropping columns: {str(e)}")
    
    def rename_columns(self, mapping: Dict[str, str]) -> 'CSVCleaner':
        try:
            self.df = self.df.rename(columns=mapping)
            return self
        except Exception as e:
            raise Exception(f"Error renaming columns: {str(e)}")
    
    def filter_rows(self, condition: Callable) -> 'CSVCleaner':
        try:
            self.df = self.df[condition(self.df)]
            return self
        except Exception as e:
            raise Exception(f"Error filtering rows: {str(e)}")
    
    def strip_whitespace(self, columns: Optional[List[str]] = None) -> 'CSVCleaner':
        try:
            cols = columns or self.df.select_dtypes(include=['object']).columns.tolist()
            for col in cols:
                if col in self.df.columns:
                    self.df[col] = self.df[col].astype(str).str.strip()
            return self
        except Exception as e:
            raise Exception(f"Error stripping whitespace: {str(e)}")
    
    def standardize_case(self, columns: List[str], case: str = 'lower') -> 'CSVCleaner':
        try:
            for col in columns:
                if col not in self.df.columns:
                    continue
                
                if case == 'lower':
                    self.df[col] = self.df[col].astype(str).str.lower()
                elif case == 'upper':
                    self.df[col] = self.df[col].astype(str).str.upper()
                elif case == 'title':
                    self.df[col] = self.df[col].astype(str).str.title()
                else:
                    raise ValueError(f"Unknown case: {case}")
            
            return self
        except Exception as e:
            raise Exception(f"Error standardizing case: {str(e)}")
    
    def replace_values(self, column: str, mapping: Dict) -> 'CSVCleaner':
        try:
            if column not in self.df.columns:
                raise ValueError(f"Column '{column}' not found")
            
            self.df[column] = self.df[column].replace(mapping)
            return self
        except Exception as e:
            raise Exception(f"Error replacing values: {str(e)}")
    
    def validate(self, rules: Dict[str, Callable]) -> List[int]:
        invalid_rows = []
        try:
            for col, rule in rules.items():
                if col not in self.df.columns:
                    raise ValueError(f"Column '{col}' not found")
                
                mask = ~self.df[col].apply(rule)
                invalid_rows.extend(self.df[mask].index.tolist())
            
            return list(set(invalid_rows))
        except Exception as e:
            raise Exception(f"Error validating data: {str(e)}")
    
    def get_summary(self) -> Dict:
        if self.df is None:
            return {}
        
        return {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'dtypes': self.df.dtypes.astype(str).to_dict(),
            'memory_usage': self.df.memory_usage(deep=True).sum()
        }
    
    def save(self, output_path: str, **kwargs) -> None:
        try:
            if self.df is None:
                raise ValueError("No data to save")
            
            self.df.to_csv(output_path, index=False, encoding=self.encoding, **kwargs)
            self.logger.info(f"Saved to {output_path}")
        except Exception as e:
            raise Exception(f"Error saving CSV: {str(e)}")
    
    def get_dataframe(self) -> pd.DataFrame:
        return self.df.copy() if self.df is not None else pd.DataFrame()