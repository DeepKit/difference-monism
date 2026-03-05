import sqlite3
import inspect
from typing import Any, List, Dict, Optional, Type, Union
from datetime import datetime
import json


class Field:
    def __init__(self, field_type: str, primary_key: bool = False, 
                 auto_increment: bool = False, nullable: bool = True,
                 unique: bool = False, default: Any = None):
        self.field_type = field_type
        self.primary_key = primary_key
        self.auto_increment = auto_increment
        self.nullable = nullable
        self.unique = unique
        self.default = default
        self.name = None

    def to_sql(self) -> str:
        sql_parts = [f"{self.name} {self.field_type}"]
        if self.primary_key:
            sql_parts.append("PRIMARY KEY")
        if self.auto_increment:
            sql_parts.append("AUTOINCREMENT")
        if not self.nullable and not self.primary_key:
            sql_parts.append("NOT NULL")
        if self.unique and not self.primary_key:
            sql_parts.append("UNIQUE")
        if self.default is not None and not self.auto_increment:
            sql_parts.append(f"DEFAULT {self._format_default()}")
        return " ".join(sql_parts)

    def _format_default(self) -> str:
        if isinstance(self.default, str):
            return f"'{self.default}'"
        elif isinstance(self.default, bool):
            return "1" if self.default else "0"
        return str(self.default)


class IntegerField(Field):
    def __init__(self, primary_key: bool = False, auto_increment: bool = False,
                 nullable: bool = True, unique: bool = False, default: Any = None):
        super().__init__("INTEGER", primary_key, auto_increment, nullable, unique, default)


class TextField(Field):
    def __init__(self, nullable: bool = True, unique: bool = False, default: Any = None):
        super().__init__("TEXT", nullable=nullable, unique=unique, default=default)


class RealField(Field):
    def __init__(self, nullable: bool = True, unique: bool = False, default: Any = None):
        super().__init__("REAL", nullable=nullable, unique=unique, default=default)


class BlobField(Field):
    def __init__(self, nullable: bool = True, default: Any = None):
        super().__init__("BLOB", nullable=nullable, default=default)


class DateTimeField(Field):
    def __init__(self, nullable: bool = True, auto_now: bool = False, 
                 auto_now_add: bool = False, default: Any = None):
        super().__init__("TEXT", nullable=nullable, default=default)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add


class JSONField(Field):
    def __init__(self, nullable: bool = True, default: Any = None):
        super().__init__("TEXT", nullable=nullable, default=default)


class QuerySet:
    def __init__(self, model_class: Type['Model'], db: 'SimpleORM'):
        self.model_class = model_class
        self.db = db
        self._where_clauses = []
        self._where_params = []
        self._order_by = []
        self._limit_value = None
        self._offset_value = None

    def filter(self, **kwargs) -> 'QuerySet':
        for key, value in kwargs.items():
            if '__' in key:
                field, op = key.split('__', 1)
                if op == 'gt':
                    self._where_clauses.append(f"{field} > ?")
                elif op == 'gte':
                    self._where_clauses.append(f"{field} >= ?")
                elif op == 'lt':
                    self._where_clauses.append(f"{field} < ?")
                elif op == 'lte':
                    self._where_clauses.append(f"{field} <= ?")
                elif op == 'ne':
                    self._where_clauses.append(f"{field} != ?")
                elif op == 'like':
                    self._where_clauses.append(f"{field} LIKE ?")
                elif op == 'in':
                    placeholders = ','.join(['?' for _ in value])
                    self._where_clauses.append(f"{field} IN ({placeholders})")
                    self._where_params.extend(value)
                    continue
                else:
                    raise ValueError(f"不支持的操作符: {op}")
                self._where_params.append(value)
            else:
                self._where_clauses.append(f"{key} = ?")
                self._where_params.append(value)
        return self

    def order_by(self, *fields) -> 'QuerySet':
        for field in fields:
            if field.startswith('-'):
                self._order_by.append(f"{field[1:]} DESC")
            else:
                self._order_by.append(f"{field} ASC")
        return self

    def limit(self, value: int) -> 'QuerySet':
        self._limit_value = value
        return self

    def offset(self, value: int) -> 'QuerySet':
        self._offset_value = value
        return self

    def all(self) -> List['Model']:
        return list(self)

    def first(self) -> Optional['Model']:
        results = self.limit(1).all()
        return results[0] if results else None

    def count(self) -> int:
        query = f"SELECT COUNT(*) FROM {self.model_class._table_name}"
        if self._where_clauses:
            query += " WHERE " + " AND ".join(self._where_clauses)
        
        cursor = self.db.conn.cursor()
        cursor.execute(query, self._where_params)
        return cursor.fetchone()[0]

    def delete(self) -> int:
        query = f"DELETE FROM {self.model_class._table_name}"
        if self._where_clauses:
            query += " WHERE " + " AND ".join(self._where_clauses)
        
        cursor = self.db.conn.cursor()
        cursor.execute(query, self._where_params)
        self.db.conn.commit()
        return cursor.rowcount

    def __iter__(self):
        query = f"SELECT * FROM {self.model_class._table_name}"
        if self._where_clauses:
            query += " WHERE " + " AND ".join(self._where_clauses)
        if self._order_by:
            query += " ORDER BY " + ", ".join(self._order_by)
        if self._limit_value is not None:
            query += f" LIMIT {self._limit_value}"
        if self._offset_value is not None:
            query += f" OFFSET {self._offset_value}"
        
        cursor = self.db.conn.cursor()
        cursor.execute(query, self._where_params)
        
        for row in cursor.fetchall():
            yield self.model_class._from_db_row(row, self.db)


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return super().__new__(mcs, name, bases, attrs)
        
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                value.name = key
                fields[key] = value
        
        attrs['_fields'] = fields
        attrs['_table_name'] = attrs.get('_table_name', name.lower())
        
        return super().__new__(mcs, name, bases, attrs)


class Model(metaclass=ModelMeta):
    _fields: Dict[str, Field] = {}
    _table_name: str = ''
    _db: Optional['SimpleORM'] = None

    def __init__(self, **kwargs):
        self._db = None
        for field_name, field in self._fields.items():
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name])
            elif field.default is not None:
                setattr(self, field_name, field.default)
            else:
                setattr(self, field_name, None)

    @classmethod
    def _from_db_row(cls, row: tuple, db: 'SimpleORM') -> 'Model':
        instance = cls()
        instance._db = db
        field_names = list(cls._fields.keys())
        for i, field_name in enumerate(field_names):
            field = cls._fields[field_name]
            value = row[i]
            
            if isinstance(field, DateTimeField) and value:
                try:
                    value = datetime.fromisoformat(value)
                except:
                    pass
            elif isinstance(field, JSONField) and value:
                try:
                    value = json.loads(value)
                except:
                    pass
            
            setattr(instance, field_name, value)
        return instance

    def save(self) -> 'Model':
        if not self._db:
            raise RuntimeError("模型实例未关联到数据库")
        
        pk_field = self._get_pk_field()
        pk_value = getattr(self, pk_field.name) if pk_field else None
        
        if pk_value is not None and not pk_field.auto_increment:
            existing = self._db.get(self.__class__, **{pk_field.name: pk_value})
            if existing:
                return self._update()
        
        return self._insert()

    def _insert(self) -> 'Model':
        fields_to_insert = {}
        for field_name, field in self._fields.items():
            if field.auto_increment:
                continue
            
            value = getattr(self, field_name)
            
            if isinstance(field, DateTimeField):
                if field.auto_now or field.auto_now_add:
                    value = datetime.now()
                    setattr(self, field_name, value)
                if isinstance(value, datetime):
                    value = value.isoformat()
            elif isinstance(field, JSONField) and value is not None:
                value = json.dumps(value)
            
            fields_to_insert[field_name] = value
        
        columns = ', '.join(fields_to_insert.keys())
        placeholders = ', '.join(['?' for _ in fields_to_insert])
        query = f"INSERT INTO {self._table_name} ({columns}) VALUES ({placeholders})"
        
        cursor = self._db.conn.cursor()
        cursor.execute(query, list(fields_to_insert.values()))
        self._db.conn.commit()
        
        pk_field = self._get_pk_field()
        if pk_field and pk_field.auto_increment:
            setattr(self, pk_field.name, cursor.lastrowid)
        
        return self

    def _update(self) -> 'Model':
        pk_field = self._get_pk_field()
        if not pk_field:
            raise ValueError("无法更新没有主键的模型")
        
        pk_value = getattr(self, pk_field.name)
        fields_to_update = {}
        
        for field_name, field in self._fields.items():
            if field.primary_key:
                continue
            
            value = getattr(self, field_name)
            
            if isinstance(field, DateTimeField):
                if field.auto_now:
                    value = datetime.now()
                    setattr(self, field_name, value)
                if isinstance(value, datetime):
                    value = value.isoformat()
            elif isinstance(field, JSONField) and value is not None:
                value = json.dumps(value)
            
            fields_to_update[field_name] = value
        
        set_clause = ', '.join([f"{k} = ?" for k in fields_to_update.keys()])
        query = f"UPDATE {self._table_name} SET {set_clause} WHERE {pk_field.name} = ?"
        
        cursor = self._db.conn.cursor()
        cursor.execute(query, list(fields_to_update.values()) + [pk_value])
        self._db.conn.commit()
        
        return self

    def delete(self) -> bool:
        if not self._db:
            raise RuntimeError("模型实例未关联到数据库")
        
        pk_field = self._get_pk_field()
        if not pk_field:
            raise ValueError("无法删除没有主键的模型")
        
        pk_value = getattr(self, pk_field.name)
        if pk_value is None:
            raise ValueError("主键值为空，无法删除")
        
        query = f"DELETE FROM {self._table_name} WHERE {pk_field.name} = ?"
        cursor = self._db.conn.cursor()
        cursor.execute(query, (pk_value,))
        self._db.conn.commit()
        
        return cursor.rowcount > 0

    @classmethod
    def _get_pk_field(cls) -> Optional[Field]:
        for field in cls._fields.values():
            if field.primary_key:
                return field
        return None

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for field_name in self._fields.keys():
            value = getattr(self, field_name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[field_name] = value
        return result


class SimpleORM:
    def __init__(self, db_path: str = ':memory:'):
        self.db_path = db_path
        self.conn = None
        self._connect()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise RuntimeError(f"数据库连接失败: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def create_table(self, model_class: Type[Model], drop_if_exists: bool = False):
        if drop_if_exists:
            self.drop_table(model_class)
        
        fields_sql = []
        for field in model_class._fields.values():
            fields_sql.append(field.to_sql())
        
        query = f"CREATE TABLE IF NOT EXISTS {model_class._table_name} ({', '.join(fields_sql)})"
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"创建表失败: {e}")

    def drop_table(self, model_class: Type[Model]):
        query = f"DROP TABLE IF EXISTS {model_class._table_name}"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"删除表失败: {e}")

    def create(self, model_class: Type[Model], **kwargs) -> Model:
        instance = model_class(**kwargs)
        instance._db = self
        return instance.save()

    def get(self, model_class: Type[Model], **kwargs) -> Optional[Model]:
        return self.filter(model_class, **kwargs).first()

    def filter(self, model_class: Type[Model], **kwargs) -> QuerySet:
        queryset = QuerySet(model_class, self)
        if kwargs:
            queryset = queryset.filter(**kwargs)
        return queryset

    def all(self, model_class: Type[Model]) -> List[Model]:
        return self.filter(model_class).all()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"SQL执行失败: {e}")

    def begin_transaction(self):
        self.conn.execute("BEGIN TRANSACTION")

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()