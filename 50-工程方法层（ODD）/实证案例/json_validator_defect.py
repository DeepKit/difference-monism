
import json
import re
from typing import Any, Dict, List, Optional, Union
from enum import Enum


class ValidationError(Exception):
    """JSON验证错误"""
    pass


class DataType(Enum):
    """支持的数据类型"""
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"


class JSONValidator:
    """JSON数据验证器"""
    
    def __init__(self, schema: Optional[Dict] = None):
        self.schema = schema
        self.errors = []
    
    def validate(self, data: Union[str, Dict, List]) -> bool:
        """验证JSON数据"""
        self.errors = []
        
        # 如果是字符串，先解析
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                self.errors.append(f"无效的JSON格式: {str(e)}")
                return False
        
        # 如果有schema，进行schema验证
        if self.schema:
            self._validate_schema(data, self.schema, "root")
        
        return len(self.errors) == 0
    
    def _validate_schema(self, data: Any, schema: Dict, path: str):
        """根据schema验证数据"""
        
        # 验证类型
        if "type" in schema:
            if not self._validate_type(data, schema["type"], path):
                return
        
        # 验证必填字段
        if schema.get("type") == "object" and "required" in schema:
            self._validate_required(data, schema["required"], path)
        
        # 验证对象属性
        if schema.get("type") == "object" and "properties" in schema:
            self._validate_properties(data, schema["properties"], path)
        
        # 验证数组项
        if schema.get("type") == "array" and "items" in schema:
            self._validate_array_items(data, schema["items"], path)
        
        # 验证枚举值
        if "enum" in schema:
            self._validate_enum(data, schema["enum"], path)
        
        # 验证字符串
        if schema.get("type") == "string":
            self._validate_string(data, schema, path)
        
        # 验证数字
        if schema.get("type") in ["number", "integer"]:
            self._validate_number(data, schema, path)
        
        # 验证数组
        if schema.get("type") == "array":
            self._validate_array(data, schema, path)
    
    def _validate_type(self, data: Any, expected_type: str, path: str) -> bool:
        """验证数据类型"""
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None)
        }
        
        if expected_type not in type_map:
            self.errors.append(f"{path}: 未知的类型 '{expected_type}'")
            return False
        
        expected_python_type = type_map[expected_type]
        
        if not isinstance(data, expected_python_type):
            actual_type = type(data).__name__
            self.errors.append(f"{path}: 期望类型 '{expected_type}'，实际类型 '{actual_type}'")
            return False
        
        return True
    
    def _validate_required(self, data: Any, required: List[str], path: str):
        """验证必填字段"""
        if not isinstance(data, dict):
            return
        
        for field in required:
            if field not in data:
                self.errors.append(f"{path}: 缺少必填字段 '{field}'")
    
    def _validate_properties(self, data: Any, properties: Dict, path: str):
        """验证对象属性"""
        if not isinstance(data, dict):
            return
        
        for key, value in data.items():
            if key in properties:
                new_path = f"{path}.{key}"
                self._validate_schema(value, properties[key], new_path)
    
    def _validate_array_items(self, data: Any, items_schema: Dict, path: str):
        """验证数组项"""
        if not isinstance(data, list):
            return
        
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            self._validate_schema(item, items_schema, new_path)
    
    def _validate_enum(self, data: Any, enum_values: List, path: str):
        """验证枚举值"""
        if data not in enum_values:
            self.errors.append(f"{path}: 值必须是 {enum_values} 之一，实际值为 '{data}'")
    
    def _validate_string(self, data: Any, schema: Dict, path: str):
        """验证字符串约束"""
        if not isinstance(data, str):
            return
        
        # 最小长度
        if "minLength" in schema and len(data) < schema["minLength"]:
            self.errors.append(f"{path}: 字符串长度不能小于 {schema['minLength']}")
        
        # 最大长度
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            self.errors.append(f"{path}: 字符串长度不能大于 {schema['maxLength']}")
        
        # 正则表达式
        if "pattern" in schema:
            if not re.match(schema["pattern"], data):
                self.errors.append(f"{path}: 字符串不匹配模式 '{schema['pattern']}'")
    
    def _validate_number(self, data: Any, schema: Dict, path: str):
        """验证数字约束"""
        if not isinstance(data, (int, float)):
            return
        
        # 最小值
        if "minimum" in schema and data < schema["minimum"]:
            self.errors.append(f"{path}: 值不能小于 {schema['minimum']}")
        
        # 最大值
        if "maximum" in schema and data > schema["maximum"]:
            self.errors.append(f"{path}: 值不能大于 {schema['maximum']}")
        
        # 排他最小值
        if "exclusiveMinimum" in schema and data <= schema["exclusiveMinimum"]:
            self.errors.append(f"{path}: 值必须大于 {schema['exclusiveMinimum']}")
        
        # 排他最大值
        if "exclusiveMaximum" in schema and data >= schema["exclusiveMaximum"]:
            self.errors.append(f"{path}: 值必须小于 {schema['exclusiveMaximum']}")
    
    def _validate_array(self, data: Any, schema: Dict, path: str):
        """验证数组约束"""
        if not isinstance(data, list):
            return
        
        # 最小项数
        if "minItems" in schema and len(data) < schema["minItems"]:
            self.errors.append(f"{path}: 数组项数不能小于 {schema['minItems']}")
        
        # 最大项数
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            self.errors.append(f"{path}: 数组项数不能大于 {schema['maxItems']}")
        
        # 唯一性
        if schema.get("uniqueItems", False):
            if len(data) != len(set(map(str, data))):
                self.errors.append(f"{path}: 数组项必须唯一")
    
    def get_errors(self) -> List[str]:
        """获取所有验证错误"""
        return self.errors


# 使用示例
if __name__ == "__main__":
    # 定义schema
    user_schema = {
        "type": "object",
        "required": ["name", "email", "age"],
        "properties": {
            "name": {
                "type": "string",
                "minLength": 2,
                "maxLength": 50
            },
            "email": {
                "type": "string",
                "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            },
            "age": {
                "type": "integer",
                "minimum": 0,
                "maximum": 150
            },
            "role": {
                "type": "string",
                "enum": ["admin", "user", "guest"]
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 10
            }
        }
    }
    
    # 创建验证器
    validator = JSONValidator(user_schema)
    
    # 验证数据
    valid_data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25,
        "role": "user",
        "tags": ["python", "developer"]
    }
    
    invalid_data = {
        "name": "李",
        "email": "invalid-email",
        "age": 200,
        "role": "superuser"
    }
    
    print("验证有效数据:")
    if validator.validate(valid_data):
        print("✓ 验证通过")
    else:
        print("✗ 验证失败:")
        for error in validator.get_errors():
            print(f"  - {error}")
    
    print("\n验证无效数据:")
    if validator.validate(invalid_data):
        print("✓ 验证通过")
    else:
        print("✗ 验证失败:")
        for error in validator.get_errors():
            print(f"  - {error}")
