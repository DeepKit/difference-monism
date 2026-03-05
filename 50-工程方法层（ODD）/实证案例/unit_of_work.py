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


# 使用示例
class User:
    """示例实体"""
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class UserRepository(Repository[User]):
    """用户仓储"""
    
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


class AppUnitOfWork(SQLAlchemyUnitOfWork):
    """应用工作单元"""
    
    def __enter__(self):
        super().__enter__()
        self.users = UserRepository(self.session)
        return self


# 使用方式
if __name__ == "__main__":
    engine = create_engine("sqlite:///example.db")
    session_factory = sessionmaker(bind=engine)
    
    # 方式1: 上下文管理器
    with AppUnitOfWork(session_factory) as uow:
        user = User(1, "张三")
        uow.users.add(user)
        uow.commit()
    
    # 方式2: 手动管理
    uow = AppUnitOfWork(session_factory)
    uow.__enter__()
    try:
        user = uow.users.get(1)
        if user:
            user.name = "李四"
            uow.users.update(user)
        uow.commit()
    except Exception as e:
        uow.rollback()
        raise
    finally:
        uow.__exit__(None, None, None)