import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from ipaddress import ip_address, IPv4Address, IPv6Address


class ValidationError(Exception):
    def __init__(self, message: str, path: str = ""):
        self.message = message
        self.path = path
        super().__init__(f"{path}: {message}" if path else message)


class JSONSchemaValidator:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.errors: List[ValidationError] = []
    
    def validate(self, data: Any, collect_errors: bool = False) -> bool:
        self.errors = []
        try:
            self._validate(data, self.schema, "")
            return len(self.errors) == 0
        except ValidationError as e:
            if not collect_errors:
                raise
            self.errors.append(e)
            return False
    
    def get_errors(self) -> List[ValidationError]:
        return self.errors
    
    def _validate(self, data: Any, schema: Dict[str, Any], path: str):
        if "type" in schema:
            self._validate_type(data, schema["type"], path)
        
        if "enum" in schema:
            self._validate_enum(data, schema["enum"], path)
        
        if "const" in schema:
            self._validate_const(data, schema["const"], path)
        
        data_type = type(data).__name__
        
        if data_type == "str" or isinstance(data, str):
            self._validate_string(data, schema, path)
        elif data_type in ["int", "float"] or isinstance(data, (int, float)):
            self._validate_number(data, schema, path)
        elif data_type == "list" or isinstance(data, list):
            self._validate_array(data, schema, path)
        elif data_type == "dict" or isinstance(data, dict):
            self._validate_object(data, schema, path)
        
        if "allOf" in schema:
            for sub_schema in schema["allOf"]:
                self._validate(data, sub_schema, path)
        
        if "anyOf" in schema:
            valid = False
            for sub_schema in schema["anyOf"]:
                try:
                    self._validate(data, sub_schema, path)
                    valid = True
                    break
                except ValidationError:
                    continue
            if not valid:
                raise ValidationError("Data does not match any schema in anyOf", path)
        
        if "oneOf" in schema:
            valid_count = 0
            for sub_schema in schema["oneOf"]:
                try:
                    self._validate(data, sub_schema, path)
                    valid_count += 1
                except ValidationError:
                    continue
            if valid_count != 1:
                raise ValidationError(f"Data matches {valid_count} schemas in oneOf, expected exactly 1", path)
        
        if "not" in schema:
            try:
                self._validate(data, schema["not"], path)
                raise ValidationError("Data matches schema in 'not'", path)
            except ValidationError:
                pass
    
    def _validate_type(self, data: Any, expected_type: Union[str, List[str]], path: str):
        if isinstance(expected_type, list):
            valid = any(self._check_type(data, t) for t in expected_type)
            if not valid:
                raise ValidationError(f"Expected type {expected_type}, got {type(data).__name__}", path)
        else:
            if not self._check_type(data, expected_type):
                raise ValidationError(f"Expected type {expected_type}, got {type(data).__name__}", path)
    
    def _check_type(self, data: Any, expected_type: str) -> bool:
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None)
        }
        
        if expected_type == "integer" and isinstance(data, bool):
            return False
        
        if expected_type == "number" and isinstance(data, bool):
            return False
        
        expected_python_type = type_map.get(expected_type)
        if expected_python_type is None:
            return False
        
        return isinstance(data, expected_python_type)
    
    def _validate_enum(self, data: Any, enum_values: List[Any], path: str):
        if data not in enum_values:
            raise ValidationError(f"Value must be one of {enum_values}", path)
    
    def _validate_const(self, data: Any, const_value: Any, path: str):
        if data != const_value:
            raise ValidationError(f"Value must be {const_value}", path)
    
    def _validate_string(self, data: str, schema: Dict[str, Any], path: str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            raise ValidationError(f"String length {len(data)} is less than minLength {schema['minLength']}", path)
        
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            raise ValidationError(f"String length {len(data)} is greater than maxLength {schema['maxLength']}", path)
        
        if "pattern" in schema:
            if not re.search(schema["pattern"], data):
                raise ValidationError(f"String does not match pattern {schema['pattern']}", path)
        
        if "format" in schema:
            self._validate_format(data, schema["format"], path)
    
    def _validate_format(self, data: str, format_type: str, path: str):
        validators = {
            "email": self._validate_email,
            "date": self._validate_date,
            "date-time": self._validate_datetime,
            "uri": self._validate_uri,
            "ipv4": self._validate_ipv4,
            "ipv6": self._validate_ipv6,
        }
        
        validator = validators.get(format_type)
        if validator:
            validator(data, path)
    
    def _validate_email(self, data: str, path: str):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, data):
            raise ValidationError(f"Invalid email format", path)
    
    def _validate_date(self, data: str, path: str):
        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(f"Invalid date format, expected YYYY-MM-DD", path)
    
    def _validate_datetime(self, data: str, path: str):
        try:
            datetime.fromisoformat(data.replace('Z', '+00:00'))
        except ValueError:
            raise ValidationError(f"Invalid date-time format", path)
    
    def _validate_uri(self, data: str, path: str):
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(pattern, data):
            raise ValidationError(f"Invalid URI format", path)
    
    def _validate_ipv4(self, data: str, path: str):
        try:
            addr = ip_address(data)
            if not isinstance(addr, IPv4Address):
                raise ValidationError(f"Invalid IPv4 address", path)
        except ValueError:
            raise ValidationError(f"Invalid IPv4 address", path)
    
    def _validate_ipv6(self, data: str, path: str):
        try:
            addr = ip_address(data)
            if not isinstance(addr, IPv6Address):
                raise ValidationError(f"Invalid IPv6 address", path)
        except ValueError:
            raise ValidationError(f"Invalid IPv6 address", path)
    
    def _validate_number(self, data: Union[int, float], schema: Dict[str, Any], path: str):
        if "minimum" in schema:
            if schema.get("exclusiveMinimum", False):
                if data <= schema["minimum"]:
                    raise ValidationError(f"Value {data} is not greater than minimum {schema['minimum']}", path)
            else:
                if data < schema["minimum"]:
                    raise ValidationError(f"Value {data} is less than minimum {schema['minimum']}", path)
        
        if "maximum" in schema:
            if schema.get("exclusiveMaximum", False):
                if data >= schema["maximum"]:
                    raise ValidationError(f"Value {data} is not less than maximum {schema['maximum']}", path)
            else:
                if data > schema["maximum"]:
                    raise ValidationError(f"Value {data} is greater than maximum {schema['maximum']}", path)
        
        if "multipleOf" in schema:
            if data % schema["multipleOf"] != 0:
                raise ValidationError(f"Value {data} is not a multiple of {schema['multipleOf']}", path)
    
    def _validate_array(self, data: List[Any], schema: Dict[str, Any], path: str):
        if "minItems" in schema and len(data) < schema["minItems"]:
            raise ValidationError(f"Array length {len(data)} is less than minItems {schema['minItems']}", path)
        
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            raise ValidationError(f"Array length {len(data)} is greater than maxItems {schema['maxItems']}", path)
        
        if "uniqueItems" in schema and schema["uniqueItems"]:
            if len(data) != len(set(str(item) for item in data)):
                raise ValidationError(f"Array items are not unique", path)
        
        if "items" in schema:
            items_schema = schema["items"]
            if isinstance(items_schema, dict):
                for i, item in enumerate(data):
                    self._validate(item, items_schema, f"{path}[{i}]")
            elif isinstance(items_schema, list):
                for i, item in enumerate(data):
                    if i < len(items_schema):
                        self._validate(item, items_schema[i], f"{path}[{i}]")
        
        if "contains" in schema:
            valid = False
            for i, item in enumerate(data):
                try:
                    self._validate(item, schema["contains"], f"{path}[{i}]")
                    valid = True
                    break
                except ValidationError:
                    continue
            if not valid:
                raise ValidationError(f"Array does not contain item matching schema", path)
    
    def _validate_object(self, data: Dict[str, Any], schema: Dict[str, Any], path: str):
        if "required" in schema:
            for required_prop in schema["required"]:
                if required_prop not in data:
                    raise ValidationError(f"Required property '{required_prop}' is missing", path)
        
        if "minProperties" in schema and len(data) < schema["minProperties"]:
            raise ValidationError(f"Object has {len(data)} properties, minimum is {schema['minProperties']}", path)
        
        if "maxProperties" in schema and len(data) > schema["maxProperties"]:
            raise ValidationError(f"Object has {len(data)} properties, maximum is {schema['maxProperties']}", path)
        
        if "properties" in schema:
            for prop_name, prop_value in data.items():
                if prop_name in schema["properties"]:
                    prop_path = f"{path}.{prop_name}" if path else prop_name
                    self._validate(prop_value, schema["properties"][prop_name], prop_path)
        
        if "additionalProperties" in schema:
            additional = schema["additionalProperties"]
            defined_props = set(schema.get("properties", {}).keys())
            pattern_props = set(schema.get("patternProperties", {}).keys())
            
            for prop_name, prop_value in data.items():
                if prop_name not in defined_props:
                    matched_pattern = False
                    for pattern in pattern_props:
                        if re.search(pattern, prop_name):
                            matched_pattern = True
                            break
                    
                    if not matched_pattern:
                        if additional is False:
                            raise ValidationError(f"Additional property '{prop_name}' is not allowed", path)
                        elif isinstance(additional, dict):
                            prop_path = f"{path}.{prop_name}" if path else prop_name
                            self._validate(prop_value, additional, prop_path)
        
        if "patternProperties" in schema:
            for prop_name, prop_value in data.items():
                for pattern, pattern_schema in schema["patternProperties"].items():
                    if re.search(pattern, prop_name):
                        prop_path = f"{path}.{prop_name}" if path else prop_name
                        self._validate(prop_value, pattern_schema, prop_path)
        
        if "dependencies" in schema:
            for prop_name, dependency in schema["dependencies"].items():
                if prop_name in data:
                    if isinstance(dependency, list):
                        for dep_prop in dependency:
                            if dep_prop not in data:
                                raise ValidationError(f"Property '{prop_name}' requires '{dep_prop}'", path)
                    elif isinstance(dependency, dict):
                        self._validate(data, dependency, path)