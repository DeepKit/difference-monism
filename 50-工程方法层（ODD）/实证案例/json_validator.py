
import json
from typing import Any, Dict, List, Optional, Union
from enum import Enum


class ValidationError(Exception):
    """JSON验证错误"""
    def __init__(self, message: str, path: str = "", value: Any = None):
        self.message = message
        self.path = path
        self.value = value
        super().__init__(self.format_error())
    
    def format_error(self) -> str:
        error_msg = f"验证错误: {self.message}"
        if self.path:
            error_msg += f" (路径: {self.path})"
        if self.value is not None:
            error_msg += f" (值: {self.value})"
        return error_msg


class DataType(Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"


class JSONValidator:
    """JSON验证器"""
    
    def __init__(self, schema: Optional[Dict[str, Any]] = None):
        self.schema = schema
        self.errors: List[ValidationError] = []
    
    def validate_json(self, json_string: str) -> bool:
        """验证JSON字符串格式"""
        try:
            json.loads(json_string)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(
                ValidationError(f"JSON格式错误: {str(e)}", path=f"位置 {e.pos}")
            )
            return False
    
    def validate(self, data: Any, schema: Optional[Dict[str, Any]] = None) -> bool:
        """验证数据是否符合Schema"""
        self.errors.clear()
        schema = schema or self.schema
        
        if schema is None:
            raise ValueError("未提供验证Schema")
        
        try:
            self._validate_value(data, schema, "root")
            return len(self.errors) == 0
        except Exception as e:
            self.errors.append(ValidationError(f"验证过程出错: {str(e)}"))
            return False
    
    def _validate_value(self, value: Any, schema: Dict[str, Any], path: str):
        """验证单个值"""
        # 类型验证
        if "type" in schema:
            self._validate_type(value, schema["type"], path)
        
        # 枚举验证
        if "enum" in schema:
            if value not in schema["enum"]:
                self.errors.append(
                    ValidationError(f"值必须是 {schema['enum']} 之一", path, value)
                )
        
        # 根据类型进行特定验证
        value_type = type(value).__name__
        
        if isinstance(value, str):
            self._validate_string(value, schema, path)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            self._validate_number(value, schema, path)
        elif isinstance(value, bool):
            self._validate_boolean(value, schema, path)
        elif isinstance(value, list):
            self._validate_array(value, schema, path)
        elif isinstance(value, dict):
            self._validate_object(value, schema, path)
        elif value is None:
            self._validate_null(value, schema, path)
    
    def _validate_type(self, value: Any, expected_type: Union[str, List[str]], path: str):
        """验证数据类型"""
        if isinstance(expected_type, list):
            types = expected_type
        else:
            types = [expected_type]
        
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None)
        }
        
        valid = False
        for t in types:
            expected_python_type = type_map.get(t)
            if expected_python_type:
                if t == "number":
                    valid = isinstance(value, (int, float)) and not isinstance(value, bool)
                elif t == "integer":
                    valid = isinstance(value, int) and not isinstance(value, bool)
                else:
                    valid = isinstance(value, expected_python_type)
                
                if valid:
                    break
        
        if not valid:
            self.errors.append(
                ValidationError(f"类型错误，期望 {expected_type}，实际 {type(value).__name__}", path, value)
            )
    
    def _validate_string(self, value: str, schema: Dict[str, Any], path: str):
        """验证字符串"""
        if "minLength" in schema and len(value) < schema["minLength"]:
            self.errors.append(
                ValidationError(f"字符串长度不能小于 {schema['minLength']}", path, value)
            )
        
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            self.errors.append(
                ValidationError(f"字符串长度不能大于 {schema['maxLength']}", path, value)
            )
        
        if "pattern" in schema:
            import re
            if not re.match(schema["pattern"], value):
                self.errors.append(
                    ValidationError(f"字符串不匹配模式 {schema['pattern']}", path, value)
                )
    
    def _validate_number(self, value: Union[int, float], schema: Dict[str, Any], path: str):
        """验证数字"""
        if "minimum" in schema and value < schema["minimum"]:
            self.errors.append(
                ValidationError(f"数值不能小于 {schema['minimum']}", path, value)
            )
        
        if "maximum" in schema and value > schema["maximum"]:
            self.errors.append(
                ValidationError(f"数值不能大于 {schema['maximum']}", path, value)
            )
        
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            self.errors.append(
                ValidationError(f"数值必须大于 {schema['exclusiveMinimum']}", path, value)
            )
        
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            self.errors.append(
                ValidationError(f"数值必须小于 {schema['exclusiveMaximum']}", path, value)
            )
        
        if "multipleOf" in schema and value % schema["multipleOf"] != 0:
            self.errors.append(
                ValidationError(f"数值必须是 {schema['multipleOf']} 的倍数", path, value)
            )
    
    def _validate_boolean(self, value: bool, schema: Dict[str, Any], path: str):
        """验证布尔值"""
        pass
    
    def _validate_array(self, value: List[Any], schema: Dict[str, Any], path: str):
        """验证数组"""
        if "minItems" in schema and len(value) < schema["minItems"]:
            self.errors.append(
                ValidationError(f"数组元素数量不能小于 {schema['minItems']}", path, value)
            )
        
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            self.errors.append(
                ValidationError(f"数组元素数量不能大于 {schema['maxItems']}", path, value)
            )
        
        if "uniqueItems" in schema and schema["uniqueItems"]:
            if len(value) != len(set(str(v) for v in value)):
                self.errors.append(
                    ValidationError("数组元素必须唯一", path, value)
                )
        
        if "items" in schema:
            for i, item in enumerate(value):
                self._validate_value(item, schema["items"], f"{path}[{i}]")
    
    def _validate_object(self, value: Dict[str, Any], schema: Dict[str, Any], path: str):
        """验证对象"""
        # 必需属性验证
        if "required" in schema:
            for required_key in schema["required"]:
                if required_key not in value:
                    self.errors.append(
                        ValidationError(f"缺少必需属性 '{required_key}'", path)
                    )
        
        # 属性验证
        if "properties" in schema:
            for key, val in value.items():
                if key in schema["properties"]:
                    self._validate_value(val, schema["properties"][key], f"{path}.{key}")
                elif "additionalProperties" in schema:
                    if schema["additionalProperties"] is False:
                        self.errors.append(
                            ValidationError(f"不允许额外属性 '{key}'", path)
                        )
                    elif isinstance(schema["additionalProperties"], dict):
                        self._validate_value(val, schema["additionalProperties"], f"{path}.{key}")
        
        # 属性数量验证
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            self.errors.append(
                ValidationError(f"对象属性数量不能小于 {schema['minProperties']}", path)
            )
        
        if "maxProperties" in schema and len(value) > schema["maxProperties"]:
            self.errors.append(
                ValidationError(f"对象属性数量不能大于 {schema['maxProperties']}", path)
            )
    
    def _validate_null(self, value: None, schema: Dict[str, Any], path: str):
        """验证null值"""
        pass
    
    def get_errors(self) -> List[str]:
        """获取所有错误信息"""
        return [error.format_error() for error in self.errors]
    
    def get_error_details(self) -> List[Dict[str, Any]]:
        """获取详细错误信息"""
        return [
            {
                "message": error.message,
                "path": error.path,
                "value": error.value
            }
            for error in self.errors
        ]


# 使用示例
if __name__ == "__main__":
    # Schema定义
    schema = {
        "type": "object",
        "required": ["name", "age"],
        "properties": {
            "name": {
                "type": "string",
                "minLength": 2,
                "maxLength": 50
            },
            "age": {
                "type": "integer",
                "minimum": 0,
                "maximum": 150
            },
            "email": {
                "type": "string",
                "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": True
            }
        }
    }
    
    validator = JSONValidator(schema)
    
    # 测试数据
    test_data = {
        "name": "张三",
        "age": 25,
        "email": "zhangsan@example.com",
        "tags": ["python", "javascript"]
    }
    
    # 验证
    if validator.validate(test_data):
        print("验证通过")
    else:
        print("验证失败:")
        for error in validator.get_errors():
            print(f"  - {error}")
