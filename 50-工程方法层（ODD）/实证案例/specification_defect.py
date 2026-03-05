from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Specification(ABC, Generic[T]):
    """规约模式基类"""
    
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """判断候选对象是否满足规约"""
        pass
    
    def and_(self, other: 'Specification[T]') -> 'Specification[T]':
        """与操作"""
        return AndSpecification(self, other)
    
    def or_(self, other: 'Specification[T]') -> 'Specification[T]':
        """或操作"""
        return OrSpecification(self, other)
    
    def not_(self) -> 'Specification[T]':
        """非操作"""
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    """与规约"""
    
    def __init__(self, left: Specification[T], right: Specification[T]):
        self.left = left
        self.right = right
    
    def is_satisfied_by(self, candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(candidate)


class OrSpecification(Specification[T]):
    """或规约"""
    
    def __init__(self, left: Specification[T], right: Specification[T]):
        self.left = left
        self.right = right
    
    def is_satisfied_by(self, candidate: T) -> bool:
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(candidate)


class NotSpecification(Specification[T]):
    """非规约"""
    
    def __init__(self, spec: Specification[T]):
        self.spec = spec
    
    def is_satisfied_by(self, candidate: T) -> bool:
        return not self.spec.is_satisfied_by(candidate)


# 示例：用户规约
class User:
    def __init__(self, name: str, age: int, is_premium: bool):
        self.name = name
        self.age = age
        self.is_premium = is_premium


class AgeSpecification(Specification[User]):
    """年龄规约"""
    
    def __init__(self, min_age: int, max_age: int = None):
        self.min_age = min_age
        self.max_age = max_age
    
    def is_satisfied_by(self, candidate: User) -> bool:
        if self.max_age:
            return self.min_age <= candidate.age <= self.max_age
        return candidate.age >= self.min_age


class PremiumSpecification(Specification[User]):
    """会员规约"""
    
    def is_satisfied_by(self, candidate: User) -> bool:
        return candidate.is_premium


class NameSpecification(Specification[User]):
    """姓名规约"""
    
    def __init__(self, name: str):
        self.name = name
    
    def is_satisfied_by(self, candidate: User) -> bool:
        return candidate.name == self.name


# 使用示例
if __name__ == "__main__":
    users = [
        User("Alice", 25, True),
        User("Bob", 17, False),
        User("Charlie", 30, True),
        User("David", 22, False),
    ]
    
    # 成年用户规约
    adult_spec = AgeSpecification(18)
    
    # 会员规约
    premium_spec = PremiumSpecification()
    
    # 成年且是会员的规约
    adult_premium_spec = adult_spec.and_(premium_spec)
    
    # 未成年或非会员的规约
    young_or_non_premium = AgeSpecification(0, 17).or_(premium_spec.not_())
    
    print("成年会员用户:")
    for user in users:
        if adult_premium_spec.is_satisfied_by(user):
            print(f"  {user.name}, {user.age}岁")
    
    print("\n未成年或非会员用户:")
    for user in users:
        if young_or_non_premium.is_satisfied_by(user):
            print(f"  {user.name}, {user.age}岁, 会员: {user.is_premium}")