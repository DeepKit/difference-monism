from typing import Any, Dict, List, Union, Callable, Optional
from enum import Enum


class DeclarationType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    ANY = "any"


class DeclarationChecker:
    def __init__(self):
        self.schemas: Dict[str, Dict] = {}
        self.errors: List[str] = []
    
    def declare(self, name: str, schema: Dict[str, Any]) -> None:
        """注册声明模式"""
        self.schemas[name] = schema
    
    def check(self, name: str, data: Any) -> bool:
        """检查数据是否符合声明"""
        self.errors = []
        
        if name not in self.schemas:
            self.errors.append(f"未找到声明: {name}")
            return False
        
        schema = self.schemas[name]
        return self._validate(data, schema, name)
    
    def _validate(self, data: Any, schema: Dict, path: str = "") -> bool:
        """递归验证数据"""
        valid = True
        
        # 检查必需字段
        if "required" in schema:
            for field in schema["required"]:
                if not isinstance(data, dict) or field not in data:
                    self.errors.append(f"{path}: 缺少必需字段 '{field}'")
                    valid = False
        
        # 检查类型
        if "type" in schema:
            if not self._check_type(data, schema["type"], path):
                valid = False
        
        # 检查字段定义
        if "fields" in schema and isinstance(data, dict):
            for field_name, field_schema in schema["fields"].items():
                if field_name in data:
                    if not self._validate(data[field_name], field_schema, f"{path}.{field_name}"):
                        valid = False
        
        # 检查列表项
        if "items" in schema and isinstance(data, list):
            for i, item in enumerate(data):
                if not self._validate(item, schema["items"], f"{path}[{i}]"):
                    valid = False
        
        # 自定义验证器
        if "validator" in schema:
            try:
                if not schema["validator"](data):
                    self.errors.append(f"{path}: 自定义验证失败")
                    valid = False
            except Exception as e:
                self.errors.append(f"{path}: 验证器异常 - {str(e)}")
                valid = False
        
        # 值范围检查
        if "min" in schema and isinstance(data, (int, float)):
            if data < schema["min"]:
                self.errors.append(f"{path}: 值 {data} 小于最小值 {schema['min']}")
                valid = False
        
        if "max" in schema and isinstance(data, (int, float)):
            if data > schema["max"]:
                self.errors.append(f"{path}: 值 {data} 大于最大值 {schema['max']}")
                valid = False
        
        # 长度检查
        if "minLength" in schema and isinstance(data, (str, list)):
            if len(data) < schema["minLength"]:
                self.errors.append(f"{path}: 长度 {len(data)} 小于最小长度 {schema['minLength']}")
                valid = False
        
        if "maxLength" in schema and isinstance(data, (str, list)):
            if len(data) > schema["maxLength"]:
                self.errors.append(f"{path}: 长度 {len(data)} 大于最大长度 {schema['maxLength']}")
                valid = False
        
        # 枚举值检查
        if "enum" in schema:
            if data not in schema["enum"]:
                self.errors.append(f"{path}: 值 '{data}' 不在允许的枚举值中")
                valid = False
        
        return valid
    
    def _check_type(self, data: Any, expected_type: Union[str, DeclarationType], path: str) -> bool:
        """检查数据类型"""
        if isinstance(expected_type, str):
            expected_type = DeclarationType(expected_type)
        
        type_map = {
            DeclarationType.STRING: str,
            DeclarationType.INTEGER: int,
            DeclarationType.FLOAT: (int, float),
            DeclarationType.BOOLEAN: bool,
            DeclarationType.LIST: list,
            DeclarationType.DICT: dict,
            DeclarationType.ANY: object
        }
        
        expected_python_type = type_map.get(expected_type)
        
        if expected_type == DeclarationType.ANY:
            return True
        
        if not isinstance(data, expected_python_type):
            self.errors.append(
                f"{path}: 类型错误，期望 {expected_type.value}，实际为 {type(data).__name__}"
            )
            return False
        
        return True
    
    def get_errors(self) -> List[str]:
        """获取所有错误信息"""
        return self.errors
    
    def clear_errors(self) -> None:
        """清除错误信息"""
        self.errors = []


# 使用示例
if __name__ == "__main__":
    checker = DeclarationChecker()
    
    # 声明用户模式
    checker.declare("user", {
        "type": "dict",
        "required": ["name", "age", "email"],
        "fields": {
            "name": {
                "type": "string",
                "minLength": 2,
                "maxLength": 50
            },
            "age": {
                "type": "integer",
                "min": 0,
                "max": 150
            },
            "email": {
                "type": "string",
                "validator": lambda x: "@" in x
            },
            "role": {
                "type": "string",
                "enum": ["admin", "user", "guest"]
            }
        }
    })
    
    # 测试数据
    valid_user = {
        "name": "张三",
        "age": 25,
        "email": "zhangsan@example.com",
        "role": "user"
    }
    
    invalid_user = {
        "name": "李",
        "age": 200,
        "email": "invalid-email"
    }
    
    # 检查有效数据
    if checker.check("user", valid_user):
        print("✓ 有效用户数据")
    else:
        print("✗ 无效用户数据:")
        for error in checker.get_errors():
            print(f"  - {error}")
    
    # 检查无效数据
    if checker.check("user", invalid_user):
        print("✓ 有效用户数据")
    else:
        print("✗ 无效用户数据:")
        for error in checker.get_errors():
            print(f"  - {error}")