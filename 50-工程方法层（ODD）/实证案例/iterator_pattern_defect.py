from abc import ABC, abstractmethod
from typing import Any, List


# 迭代器接口
class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass
    
    @abstractmethod
    def next(self) -> Any:
        pass


# 集合接口
class Aggregate(ABC):
    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass


# 具体迭代器
class BookIterator(Iterator):
    def __init__(self, books: List[str]):
        self._books = books
        self._index = 0
    
    def has_next(self) -> bool:
        return self._index < len(self._books)
    
    def next(self) -> str:
        if not self.has_next():
            raise StopIteration("没有更多元素")
        book = self._books[self._index]
        self._index += 1
        return book


# 具体集合
class BookShelf(Aggregate):
    def __init__(self):
        self._books: List[str] = []
    
    def add_book(self, book: str):
        self._books.append(book)
    
    def get_book_at(self, index: int) -> str:
        return self._books[index]
    
    def get_length(self) -> int:
        return len(self._books)
    
    def create_iterator(self) -> Iterator:
        return BookIterator(self._books)


# 使用示例
if __name__ == "__main__":
    # 创建书架
    bookshelf = BookShelf()
    bookshelf.add_book("设计模式")
    bookshelf.add_book("重构")
    bookshelf.add_book("代码整洁之道")
    bookshelf.add_book("Python编程")
    
    # 使用迭代器遍历
    iterator = bookshelf.create_iterator()
    print("书架中的书籍：")
    while iterator.has_next():
        book = iterator.next()
        print(f"- {book}")
    
    # 也可以使用Python内置迭代器协议
    class BookShelfPythonic(Aggregate):
        def __init__(self):
            self._books: List[str] = []
        
        def add_book(self, book: str):
            self._books.append(book)
        
        def create_iterator(self) -> Iterator:
            return BookIterator(self._books)
        
        def __iter__(self):
            return iter(self._books)
    
    # Python风格的使用
    bookshelf2 = BookShelfPythonic()
    bookshelf2.add_book("算法导论")
    bookshelf2.add_book("深入理解计算机系统")
    
    print("\nPython风格遍历：")
    for book in bookshelf2:
        print(f"- {book}")