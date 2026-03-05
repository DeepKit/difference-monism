from abc import ABC, abstractmethod


class AbstractUser(ABC):
    """用户抽象基类"""
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_role(self) -> str:
        pass
    
    @abstractmethod
    def is_null(self) -> bool:
        pass


class RealUser(AbstractUser):
    """真实用户对象"""
    
    def __init__(self, name: str, role: str):
        self._name = name
        self._role = role
    
    def get_name(self) -> str:
        return self._name
    
    def get_role(self) -> str:
        return self._role
    
    def is_null(self) -> bool:
        return False


class NullUser(AbstractUser):
    """空用户对象"""
    
    def get_name(self) -> str:
        return "Guest"
    
    def get_role(self) -> str:
        return "None"
    
    def is_null(self) -> bool:
        return True


class UserFactory:
    """用户工厂"""
    
    _users = {
        "Alice": RealUser("Alice", "Admin"),
        "Bob": RealUser("Bob", "User"),
        "Charlie": RealUser("Charlie", "Moderator")
    }
    
    @classmethod
    def get_user(cls, name: str) -> AbstractUser:
        """获取用户，不存在则返回空对象"""
        return cls._users.get(name, NullUser())


# 使用示例
if __name__ == "__main__":
    # 获取存在的用户
    user1 = UserFactory.get_user("Alice")
    print(f"Name: {user1.get_name()}, Role: {user1.get_role()}, Is Null: {user1.is_null()}")
    
    # 获取不存在的用户，返回空对象
    user2 = UserFactory.get_user("David")
    print(f"Name: {user2.get_name()}, Role: {user2.get_role()}, Is Null: {user2.is_null()}")
    
    # 无需空值检查，直接调用方法
    for name in ["Alice", "Unknown", "Bob"]:
        user = UserFactory.get_user(name)
        print(f"{user.get_name()} - {user.get_role()}")