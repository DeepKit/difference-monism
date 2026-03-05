import sqlite3
from typing import Any, List, Optional, Type, TypeVar
from dataclasses import dataclass, fields

T = TypeVar('T', bound='Model')


class Model:
    """ORM基类"""
    _table_name: str = None
    _primary_key: str = 'id'
    
    def __init_subclass__(cls):
        if not cls._table_name:
            cls._table_name = cls.__name__.lower()


class SimpleORM:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
    
    def create_table(self, model_class: Type[T]):
        """根据模型类创建表"""
        table_name = model_class._table_name
        field_defs = []
        
        for field in fields(model_class):
            field_type = field.type
            sql_type = self._python_to_sql_type(field_type)
            
            if field.name == model_class._primary_key:
                field_defs.append(f"{field.name} {sql_type} PRIMARY KEY AUTOINCREMENT")
            else:
                field_defs.append(f"{field.name} {sql_type}")
        
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(field_defs)})"
        self.conn.execute(sql)
        self.conn.commit()
    
    def insert(self, obj: T) -> int:
        """插入记录"""
        table_name = obj._table_name
        field_names = [f.name for f in fields(obj) if f.name != obj._primary_key]
        values = [getattr(obj, name) for name in field_names]
        
        placeholders = ', '.join(['?'] * len(field_names))
        sql = f"INSERT INTO {table_name} ({', '.join(field_names)}) VALUES ({placeholders})"
        
        cursor = self.conn.execute(sql, values)
        self.conn.commit()
        return cursor.lastrowid
    
    def update(self, obj: T):
        """更新记录"""
        table_name = obj._table_name
        pk_name = obj._primary_key
        pk_value = getattr(obj, pk_name)
        
        field_names = [f.name for f in fields(obj) if f.name != pk_name]
        values = [getattr(obj, name) for name in field_names]
        
        set_clause = ', '.join([f"{name} = ?" for name in field_names])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_name} = ?"
        
        self.conn.execute(sql, values + [pk_value])
        self.conn.commit()
    
    def delete(self, model_class: Type[T], pk_value: Any):
        """删除记录"""
        table_name = model_class._table_name
        pk_name = model_class._primary_key
        sql = f"DELETE FROM {table_name} WHERE {pk_name} = ?"
        self.conn.execute(sql, (pk_value,))
        self.conn.commit()
    
    def find_by_id(self, model_class: Type[T], pk_value: Any) -> Optional[T]:
        """根据主键查询"""
        table_name = model_class._table_name
        pk_name = model_class._primary_key
        sql = f"SELECT * FROM {table_name} WHERE {pk_name} = ?"
        
        cursor = self.conn.execute(sql, (pk_value,))
        row = cursor.fetchone()
        
        return self._row_to_object(model_class, row) if row else None
    
    def find_all(self, model_class: Type[T]) -> List[T]:
        """查询所有记录"""
        table_name = model_class._table_name
        sql = f"SELECT * FROM {table_name}"
        
        cursor = self.conn.execute(sql)
        return [self._row_to_object(model_class, row) for row in cursor.fetchall()]
    
    def find_where(self, model_class: Type[T], **conditions) -> List[T]:
        """条件查询"""
        table_name = model_class._table_name
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        sql = f"SELECT * FROM {table_name} WHERE {where_clause}"
        
        cursor = self.conn.execute(sql, tuple(conditions.values()))
        return [self._row_to_object(model_class, row) for row in cursor.fetchall()]
    
    def close(self):
        """关闭连接"""
        self.conn.close()
    
    def _python_to_sql_type(self, python_type) -> str:
        """Python类型转SQL类型"""
        type_map = {
            int: 'INTEGER',
            str: 'TEXT',
            float: 'REAL',
            bool: 'INTEGER',
            bytes: 'BLOB'
        }
        return type_map.get(python_type, 'TEXT')
    
    def _row_to_object(self, model_class: Type[T], row: sqlite3.Row) -> T:
        """数据库行转对象"""
        kwargs = {key: row[key] for key in row.keys()}
        return model_class(**kwargs)


# 使用示例
@dataclass
class User(Model):
    id: int = None
    name: str = None
    email: str = None
    age: int = None


if __name__ == '__main__':
    # 初始化ORM
    orm = SimpleORM('test.db')
    
    # 创建表
    orm.create_table(User)
    
    # 插入
    user = User(name='张三', email='zhangsan@example.com', age=25)
    user_id = orm.insert(user)
    print(f"插入用户ID: {user_id}")
    
    # 查询
    found_user = orm.find_by_id(User, user_id)
    print(f"查询用户: {found_user}")
    
    # 更新
    found_user.age = 26
    orm.update(found_user)
    
    # 条件查询
    users = orm.find_where(User, name='张三')
    print(f"条件查询: {users}")
    
    # 查询所有
    all_users = orm.find_all(User)
    print(f"所有用户: {all_users}")
    
    # 删除
    orm.delete(User, user_id)
    
    # 关闭连接
    orm.close()