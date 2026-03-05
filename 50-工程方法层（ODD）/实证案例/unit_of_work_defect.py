from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    """仓储基类"""
    
    def __init__(self, session: Session):
        self.session = session
    
    @abstractmethod
    def add(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, entity: T) -> None:
        pass


class UnitOfWork(ABC):
    """工作单元抽象基类"""
    
    @abstractmethod
    def __enter__(self):
        pass
    
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    @abstractmethod
    def commit(self):
        pass
    
    @abstractmethod
    def rollback(self):
        pass


class SQLAlchemyUnitOfWork(UnitOfWork):
    """SQLAlchemy工作单元实现"""
    
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.session: Optional[Session] = None
    
    def __enter__(self):
        self.session = self.session_factory()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        self.session.close()
    
    def commit(self):
        if self.session:
            self.session.commit()
    
    def rollback(self):
        if self.session:
            self.session.rollback()
    
    def get_repository(self, repository_class: type[Repository]) -> Repository:
        """获取仓储实例"""
        return repository_class(self.session)


# 使用示例
class User:
    """用户实体示例"""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class UserRepository(Repository[User]):
    """用户仓储实现"""
    
    def add(self, entity: User) -> User:
        self.session.add(entity)
        return entity
    
    def get(self, id: int) -> Optional[User]:
        return self.session.query(User).filter_by(id=id).first()
    
    def update(self, entity: User) -> User:
        self.session.merge(entity)
        return entity
    
    def delete(self, entity: User) -> None:
        self.session.delete(entity)


# 使用方式
def example_usage():
    engine = create_engine('sqlite:///example.db')
    session_factory = sessionmaker(bind=engine)
    
    # 方式1: 使用上下文管理器
    with SQLAlchemyUnitOfWork(session_factory) as uow:
        user_repo = uow.get_repository(UserRepository)
        user = User(1, "张三")
        user_repo.add(user)
        uow.commit()
    
    # 方式2: 手动管理
    uow = SQLAlchemyUnitOfWork(session_factory)
    uow.__enter__()
    try:
        user_repo = uow.get_repository(UserRepository)
        user = user_repo.get(1)
        if user:
            user.name = "李四"
            user_repo.update(user)
        uow.commit()
    except Exception as e:
        uow.rollback()
        raise
    finally:
        uow.__exit__(None, None, None)