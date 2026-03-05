from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from dataclasses import dataclass
from uuid import uuid4

# 领域模型示例
@dataclass
class Entity:
    id: str
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())


@dataclass
class User(Entity):
    name: str
    email: str
    age: int


T = TypeVar('T', bound=Entity)


# 仓储接口
class IRepository(ABC, Generic[T]):
    
    @abstractmethod
    def add(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def get(self, id: str) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
    
    @abstractmethod
    def find(self, **criteria) -> List[T]:
        pass


# 内存仓储实现
class InMemoryRepository(IRepository[T]):
    
    def __init__(self):
        self._storage: Dict[str, T] = {}
    
    def add(self, entity: T) -> T:
        if not entity.id:
            entity.id = str(uuid4())
        self._storage[entity.id] = entity
        return entity
    
    def get(self, id: str) -> Optional[T]:
        return self._storage.get(id)
    
    def get_all(self) -> List[T]:
        return list(self._storage.values())
    
    def update(self, entity: T) -> T:
        if entity.id not in self._storage:
            raise ValueError(f"Entity with id {entity.id} not found")
        self._storage[entity.id] = entity
        return entity
    
    def delete(self, id: str) -> bool:
        if id in self._storage:
            del self._storage[id]
            return True
        return False
    
    def find(self, **criteria) -> List[T]:
        results = []
        for entity in self._storage.values():
            match = all(
                getattr(entity, key, None) == value 
                for key, value in criteria.items()
            )
            if match:
                results.append(entity)
        return results


# 用户仓储
class UserRepository(InMemoryRepository[User]):
    
    def find_by_email(self, email: str) -> Optional[User]:
        results = self.find(email=email)
        return results[0] if results else None
    
    def find_by_age_range(self, min_age: int, max_age: int) -> List[User]:
        return [
            user for user in self.get_all() 
            if min_age <= user.age <= max_age
        ]


# 使用示例
if __name__ == "__main__":
    repo = UserRepository()
    
    # 添加用户
    user1 = repo.add(User(id="", name="张三", email="zhang@example.com", age=25))
    user2 = repo.add(User(id="", name="李四", email="li@example.com", age=30))
    user3 = repo.add(User(id="", name="王五", email="wang@example.com", age=28))
    
    # 查询单个
    found = repo.get(user1.id)
    print(f"找到用户: {found}")
    
    # 查询所有
    all_users = repo.get_all()
    print(f"所有用户: {len(all_users)}个")
    
    # 按条件查询
    young_users = repo.find_by_age_range(25, 28)
    print(f"25-28岁用户: {young_users}")
    
    # 更新
    user1.age = 26
    repo.update(user1)
    
    # 删除
    repo.delete(user2.id)
    print(f"删除后剩余: {len(repo.get_all())}个用户")