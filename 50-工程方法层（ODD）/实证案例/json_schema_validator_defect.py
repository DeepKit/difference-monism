import re
from typing import Any, Dict, List, Optional


class JSONSchemaValidator:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
    
    def validate(self, data: Any) -> tuple[bool, Optional[str]]:
        """验证数据是否符合schema，返回(是否有效, 错误信息)"""
        return self._validate(data, self.schema, "root")
    
    def _validate(self, data: Any, schema: Dict[str, Any], path: str) -> tuple[bool, Optional[str]]:
        # 类型验证
        if "type" in schema:
            if not self._validate_type(data, schema["type"]):
                return False, f"{path}: 类型错误，期望 {schema['type']}"
        
        # 对象验证
        if schema.get("type") == "object" and isinstance(data, dict):
            # required字段
            if "required" in schema:
                for field in schema["required"]:
                    if field not in data:
                        return False, f"{path}: 缺少必需字段 '{field}'"
            
            # properties验证
            if "properties" in schema:
                for key, value in data.items():
                    if key in schema["properties"]:
                        valid, error = self._validate(value, schema["properties"][key], f"{path}.{key}")
                        if not valid:
                            return False, error
        
        # 数组验证
        if schema.get("type") == "array" and isinstance(data, list):
            if "items" in schema:
                for i, item in enumerate(data):
                    valid, error = self._validate(item, schema["items"], f"{path}[{i}]")
                    if not valid:
                        return False, error
            
            if "minItems" in schema and len(data) < schema["minItems"]:
                return False, f"{path}: 数组长度小于 {schema['minItems']}"
            
            if "maxItems" in schema and len(data) > schema["maxItems"]:
                return False, f"{path}: 数组长度大于 {schema['maxItems']}"
        
        # 字符串验证
        if schema.get("type") == "string" and isinstance(data, str):
            if "minLength" in schema and len(data) < schema["minLength"]:
                return False, f"{path}: 字符串长度小于 {schema['minLength']}"
            
            if "maxLength" in schema and len(data) > schema["maxLength"]:
                return False, f"{path}: 字符串长度大于 {schema['maxLength']}"
            
            if "pattern" in schema and not re.match(schema["pattern"], data):
                return False, f"{path}: 不匹配正则表达式 {schema['pattern']}"
        
        # 数字验证
        if schema.get("type") in ["number", "integer"] and isinstance(data, (int, float)):
            if "minimum" in schema and data < schema["minimum"]:
                return False, f"{path}: 值小于最小值 {schema['minimum']}"
            
            if "maximum" in schema and data > schema["maximum"]:
                return False, f"{path}: 值大于最大值 {schema['maximum']}"
        
        # enum验证
        if "enum" in schema and data not in schema["enum"]:
            return False, f"{path}: 值不在枚举范围内 {schema['enum']}"
        
        return True, None
    
    def _validate_type(self, data: Any, expected_type: str) -> bool:
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None)
        }
        return isinstance(data, type_map.get(expected_type, type(None)))


# 使用示例
if __name__ == "__main__":
    schema = {
        "type": "object",
        "required": ["name", "age"],
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "age": {"type": "integer", "minimum": 0, "maximum": 150},
            "email": {"type": "string", "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"}
        }
    }
    
    validator = JSONSchemaValidator(schema)
    
    # 有效数据
    valid_data = {"name": "张三", "age": 25, "email": "test@example.com"}
    is_valid, error = validator.validate(valid_data)
    print(f"验证结果: {is_valid}, 错误: {error}")
    
    # 无效数据
    invalid_data = {"name": "", "age": 200}
    is_valid, error = validator.validate(invalid_data)
    print(f"验证结果: {is_valid}, 错误: {error}")