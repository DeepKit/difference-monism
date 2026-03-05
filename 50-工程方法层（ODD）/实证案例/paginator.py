from enum import Enum
from typing import List, Any, Dict
from dataclasses import dataclass


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class PageResult:
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginationQuery:
    ALLOWED_SORT_FIELDS = {'id', 'created_at', 'price'}
    MIN_PAGE_SIZE = 1
    MAX_PAGE_SIZE = 100
    
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
    
    def query(self, page: int, page_size: int, sort_field: str = 'id', sort_order: str = 'asc') -> PageResult:
        page_size = self._validate_page_size(page_size)
        
        if sort_field not in self.ALLOWED_SORT_FIELDS:
            raise ValueError(f"排序字段必须是以下之一: {self.ALLOWED_SORT_FIELDS}")
        
        sort_order = sort_order.lower()
        if sort_order not in ['asc', 'desc']:
            raise ValueError("排序方向必须是 'asc' 或 'desc'")
        
        sorted_data = self._sort_data(self.data, sort_field, sort_order)
        
        total = len(sorted_data)
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        if page < 1 or (total_pages > 0 and page > total_pages):
            return PageResult(items=[], total=total, page=page, page_size=page_size, total_pages=total_pages)
        
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        items = sorted_data[start_index:end_index]
        
        return PageResult(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)
    
    def _validate_page_size(self, page_size: int) -> int:
        if page_size < self.MIN_PAGE_SIZE:
            return self.MIN_PAGE_SIZE
        if page_size > self.MAX_PAGE_SIZE:
            return self.MAX_PAGE_SIZE
        return page_size
    
    def _sort_data(self, data: List[Dict[str, Any]], sort_field: str, sort_order: str) -> List[Dict[str, Any]]:
        reverse = (sort_order == 'desc')
        return sorted(data, key=lambda x: x.get(sort_field, 0), reverse=reverse)
