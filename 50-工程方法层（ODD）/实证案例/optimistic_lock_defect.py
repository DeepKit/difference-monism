
import threading
from typing import Any, Dict, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import copy


class OptimisticLockError(Exception):
    """乐观锁冲突异常"""
    pass


@dataclass
class VersionedEntity:
    """带版本控制的实体基类"""
    version: int = 0
    updated_at: datetime = field(default_factory=datetime.now)
    
    def increment_version(self):
        """增加版本号"""
        self.version += 1
        self.updated_at = datetime.now()


class OptimisticLock:
    """乐观锁实现"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._storage: Dict[str, VersionedEntity] = {}
    
    def read(self, key: str) -> Optional[VersionedEntity]:
        """读取数据"""
        with self._lock:
            entity = self._storage.get(key)
            return copy.deepcopy(entity) if entity else None
    
    def write(self, key: str, entity: VersionedEntity, expected_version: int) -> bool:
        """
        写入数据，使用乐观锁
        
        Args:
            key: 数据键
            entity: 要写入的实体
            expected_version: 期望的版本号
            
        Returns:
            bool: 写入是否成功
            
        Raises:
            OptimisticLockError: 版本冲突时抛出
        """
        with self._lock:
            current = self._storage.get(key)
            
            # 检查版本冲突
            if current and current.version != expected_version:
                raise OptimisticLockError(
                    f"版本冲突: 期望版本 {expected_version}, 当前版本 {current.version}"
                )
            
            # 更新版本号
            entity.increment_version()
            self._storage[key] = copy.deepcopy(entity)
            return True
    
    def update(self, key: str, update_fn: Callable[[VersionedEntity], None], 
               max_retries: int = 3) -> VersionedEntity:
        """
        更新数据，自动重试
        
        Args:
            key: 数据键
            update_fn: 更新函数
            max_retries: 最大重试次数
            
        Returns:
            VersionedEntity: 更新后的实体
            
        Raises:
            OptimisticLockError: 超过最大重试次数后抛出
        """
        for attempt in range(max_retries):
            entity = self.read(key)
            if not entity:
                raise ValueError(f"键 {key} 不存在")
            
            expected_version = entity.version
            update_fn(entity)
            
            try:
                self.write(key, entity, expected_version)
                return entity
            except OptimisticLockError:
                if attempt == max_retries - 1:
                    raise
                continue
        
        raise OptimisticLockError(f"更新失败: 超过最大重试次数 {max_retries}")
    
    def create(self, key: str, entity: VersionedEntity) -> None:
        """创建新实体"""
        with self._lock:
            if key in self._storage:
                raise ValueError(f"键 {key} 已存在")
            entity.version = 0
            entity.updated_at = datetime.now()
            self._storage[key] = copy.deepcopy(entity)
    
    def delete(self, key: str, expected_version: int) -> bool:
        """
        删除数据，使用乐观锁
        
        Args:
            key: 数据键
            expected_version: 期望的版本号
            
        Returns:
            bool: 删除是否成功
            
        Raises:
            OptimisticLockError: 版本冲突时抛出
        """
        with self._lock:
            current = self._storage.get(key)
            if not current:
                return False
            
            if current.version != expected_version:
                raise OptimisticLockError(
                    f"版本冲突: 期望版本 {expected_version}, 当前版本 {current.version}"
                )
            
            del self._storage[key]
            return True


@dataclass
class Account(VersionedEntity):
    """账户示例"""
    account_id: str = ""
    balance: float = 0.0
    owner: str = ""


class OptimisticLockDecorator:
    """乐观锁装饰器实现"""
    
    @staticmethod
    def with_optimistic_lock(max_retries: int = 3):
        """
        乐观锁装饰器
        
        使用方法:
        @OptimisticLockDecorator.with_optimistic_lock(max_retries=5)
        def update_balance(lock, account_id, amount):
            # 更新逻辑
            pass
        """
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except OptimisticLockError:
                        if attempt == max_retries - 1:
                            raise
                        continue
                raise OptimisticLockError(f"操作失败: 超过最大重试次数 {max_retries}")
            return wrapper
        return decorator


class DatabaseOptimisticLock:
    """数据库乐观锁实现（SQL示例）"""
    
    @staticmethod
    def generate_update_sql(table: str, key_column: str, key_value: Any,
                           updates: Dict[str, Any], expected_version: int) -> str:
        """
        生成带乐观锁的UPDATE SQL
        
        Returns:
            str: SQL语句
        """
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        set_clause += ", version = version + 1, updated_at = CURRENT_TIMESTAMP"
        
        sql = f"""
        UPDATE {table}
        SET {set_clause}
        WHERE {key_column} = ?
        AND version = ?
        """
        return sql
    
    @staticmethod
    def check_affected_rows(affected_rows: int) -> None:
        """检查受影响的行数"""
        if affected_rows == 0:
            raise OptimisticLockError("更新失败: 版本冲突或记录不存在")


# 使用示例
if __name__ == "__main__":
    lock = OptimisticLock()
    
    # 创建账户
    account = Account(account_id="ACC001", balance=1000.0, owner="张三")
    lock.create("ACC001", account)
    
    # 读取并更新
    acc = lock.read("ACC001")
    acc.balance += 500
    lock.write("ACC001", acc, acc.version)
    
    # 使用update方法自动重试
    lock.update("ACC001", lambda acc: setattr(acc, 'balance', acc.balance - 200))
