from abc import ABC, abstractmethod
from typing import List


# Strategy Interface
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass


# Concrete Strategies
class BubbleSortStrategy(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result


class QuickSortStrategy(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class MergeSortStrategy(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result


# Context
class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort(self, data: List[int]) -> List[int]:
        return self._strategy.sort(data)


# Usage
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    
    # Using Bubble Sort
    sorter = Sorter(BubbleSortStrategy())
    print("Bubble Sort:", sorter.sort(data))
    
    # Switching to Quick Sort
    sorter.set_strategy(QuickSortStrategy())
    print("Quick Sort:", sorter.sort(data))
    
    # Switching to Merge Sort
    sorter.set_strategy(MergeSortStrategy())
    print("Merge Sort:", sorter.sort(data))