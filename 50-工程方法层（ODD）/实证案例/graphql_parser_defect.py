import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Field:
    name: str
    alias: Optional[str] = None
    arguments: Dict[str, Any] = None
    selections: List['Field'] = None
    
    def __post_init__(self):
        self.arguments = self.arguments or {}
        self.selections = self.selections or []


class GraphQLParser:
    def __init__(self, query: str):
        self.query = query.strip()
        self.pos = 0
        
    def parse(self) -> Dict[str, Any]:
        """解析GraphQL查询"""
        self._skip_whitespace()
        
        operation_type = self._parse_operation_type()
        operation_name = self._parse_operation_name()
        
        self._expect('{')
        fields = self._parse_selection_set()
        self._expect('}')
        
        return {
            'operation': operation_type,
            'name': operation_name,
            'fields': fields
        }
    
    def _parse_operation_type(self) -> str:
        """解析操作类型 (query/mutation/subscription)"""
        self._skip_whitespace()
        for op in ['query', 'mutation', 'subscription']:
            if self.query[self.pos:].startswith(op):
                self.pos += len(op)
                return op
        return 'query'
    
    def _parse_operation_name(self) -> Optional[str]:
        """解析操作名称"""
        self._skip_whitespace()
        if self._peek() == '{':
            return None
        return self._parse_name()
    
    def _parse_selection_set(self) -> List[Field]:
        """解析字段集合"""
        fields = []
        self._skip_whitespace()
        
        while self._peek() and self._peek() != '}':
            field = self._parse_field()
            if field:
                fields.append(field)
            self._skip_whitespace()
        
        return fields
    
    def _parse_field(self) -> Optional[Field]:
        """解析单个字段"""
        self._skip_whitespace()
        
        if self._peek() == '}':
            return None
        
        # 解析别名
        name = self._parse_name()
        alias = None
        
        if self._peek() == ':':
            self.pos += 1
            alias = name
            name = self._parse_name()
        
        # 解析参数
        arguments = {}
        if self._peek() == '(':
            arguments = self._parse_arguments()
        
        # 解析嵌套字段
        selections = []
        self._skip_whitespace()
        if self._peek() == '{':
            self.pos += 1
            selections = self._parse_selection_set()
            self._expect('}')
        
        return Field(name=name, alias=alias, arguments=arguments, selections=selections)
    
    def _parse_arguments(self) -> Dict[str, Any]:
        """解析参数"""
        self._expect('(')
        arguments = {}
        
        while self._peek() != ')':
            self._skip_whitespace()
            if self._peek() == ')':
                break
                
            arg_name = self._parse_name()
            self._skip_whitespace()
            self._expect(':')
            self._skip_whitespace()
            arg_value = self._parse_value()
            
            arguments[arg_name] = arg_value
            
            self._skip_whitespace()
            if self._peek() == ',':
                self.pos += 1
        
        self._expect(')')
        return arguments
    
    def _parse_value(self) -> Any:
        """解析值"""
        self._skip_whitespace()
        char = self._peek()
        
        # 字符串
        if char == '"':
            return self._parse_string()
        
        # 数字
        if char.isdigit() or char == '-':
            return self._parse_number()
        
        # 布尔值和null
        if self.query[self.pos:].startswith('true'):
            self.pos += 4
            return True
        if self.query[self.pos:].startswith('false'):
            self.pos += 5
            return False
        if self.query[self.pos:].startswith('null'):
            self.pos += 4
            return None
        
        # 列表
        if char == '[':
            return self._parse_list()
        
        # 对象
        if char == '{':
            return self._parse_object()
        
        # 变量或枚举
        return self._parse_name()
    
    def _parse_string(self) -> str:
        """解析字符串"""
        self._expect('"')
        start = self.pos
        while self.pos < len(self.query) and self.query[self.pos] != '"':
            if self.query[self.pos] == '\\':
                self.pos += 2
            else:
                self.pos += 1
        value = self.query[start:self.pos]
        self._expect('"')
        return value
    
    def _parse_number(self) -> float:
        """解析数字"""
        match = re.match(r'-?\d+\.?\d*', self.query[self.pos:])
        if match:
            value = match.group()
            self.pos += len(value)
            return float(value) if '.' in value else int(value)
        return 0
    
    def _parse_list(self) -> List[Any]:
        """解析列表"""
        self._expect('[')
        items = []
        
        while self._peek() != ']':
            self._skip_whitespace()
            if self._peek() == ']':
                break
            items.append(self._parse_value())
            self._skip_whitespace()
            if self._peek() == ',':
                self.pos += 1
        
        self._expect(']')
        return items
    
    def _parse_object(self) -> Dict[str, Any]:
        """解析对象"""
        self._expect('{')
        obj = {}
        
        while self._peek() != '}':
            self._skip_whitespace()
            if self._peek() == '}':
                break
            key = self._parse_name()
            self._skip_whitespace()
            self._expect(':')
            value = self._parse_value()
            obj[key] = value
            self._skip_whitespace()
            if self._peek() == ',':
                self.pos += 1
        
        self._expect('}')
        return obj
    
    def _parse_name(self) -> str:
        """解析名称"""
        self._skip_whitespace()
        match = re.match(r'[_A-Za-z][_0-9A-Za-z]*', self.query[self.pos:])
        if match:
            name = match.group()
            self.pos += len(name)
            return name
        return ''
    
    def _skip_whitespace(self):
        """跳过空白字符和注释"""
        while self.pos < len(self.query):
            if self.query[self.pos].isspace():
                self.pos += 1
            elif self.query[self.pos] == '#':
                while self.pos < len(self.query) and self.query[self.pos] != '\n':
                    self.pos += 1
            else:
                break
    
    def _peek(self) -> str:
        """查看当前字符"""
        return self.query[self.pos] if self.pos < len(self.query) else ''
    
    def _expect(self, char: str):
        """期望特定字符"""
        self._skip_whitespace()
        if self._peek() == char:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected '{char}' at position {self.pos}")


# 使用示例
if __name__ == '__main__':
    query = """
    query GetUser {
        user(id: 123) {
            name
            email
            posts(limit: 10) {
                title
                content
            }
        }
    }
    """
    
    parser = GraphQLParser(query)
    result = parser.parse()
    print(result)