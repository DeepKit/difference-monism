
from typing import Any, Callable, Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, field


class Operator(Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IN = "in"
    NOT_IN = "not_in"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"


@dataclass
class Condition:
    field: str
    operator: Operator
    value: Any
    
    def evaluate(self, facts: Dict[str, Any]) -> bool:
        field_value = self._get_nested_value(facts, self.field)
        
        if field_value is None:
            return False
        
        op_map = {
            Operator.EQUALS: lambda a, b: a == b,
            Operator.NOT_EQUALS: lambda a, b: a != b,
            Operator.GREATER_THAN: lambda a, b: a > b,
            Operator.LESS_THAN: lambda a, b: a < b,
            Operator.GREATER_EQUAL: lambda a, b: a >= b,
            Operator.LESS_EQUAL: lambda a, b: a <= b,
            Operator.CONTAINS: lambda a, b: b in a,
            Operator.NOT_CONTAINS: lambda a, b: b not in a,
            Operator.IN: lambda a, b: a in b,
            Operator.NOT_IN: lambda a, b: a not in b,
            Operator.STARTS_WITH: lambda a, b: str(a).startswith(str(b)),
            Operator.ENDS_WITH: lambda a, b: str(a).endswith(str(b)),
        }
        
        return op_map[self.operator](field_value, self.value)
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        keys = path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        return value


@dataclass
class Rule:
    name: str
    conditions: List[Condition]
    action: Callable[[Dict[str, Any]], None]
    priority: int = 0
    all_conditions: bool = True
    enabled: bool = True
    description: str = ""
    
    def evaluate(self, facts: Dict[str, Any]) -> bool:
        if not self.enabled:
            return False
        
        if not self.conditions:
            return True
        
        results = [condition.evaluate(facts) for condition in self.conditions]
        
        if self.all_conditions:
            return all(results)
        else:
            return any(results)
    
    def execute(self, facts: Dict[str, Any]) -> None:
        if self.evaluate(facts):
            self.action(facts)


class RuleEngine:
    def __init__(self):
        self.rules: List[Rule] = []
        self.execution_log: List[Dict[str, Any]] = []
    
    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def remove_rule(self, rule_name: str) -> bool:
        initial_count = len(self.rules)
        self.rules = [r for r in self.rules if r.name != rule_name]
        return len(self.rules) < initial_count
    
    def get_rule(self, rule_name: str) -> Optional[Rule]:
        for rule in self.rules:
            if rule.name == rule_name:
                return rule
        return None
    
    def enable_rule(self, rule_name: str) -> bool:
        rule = self.get_rule(rule_name)
        if rule:
            rule.enabled = True
            return True
        return False
    
    def disable_rule(self, rule_name: str) -> bool:
        rule = self.get_rule(rule_name)
        if rule:
            rule.enabled = False
            return True
        return False
    
    def execute(self, facts: Dict[str, Any], stop_on_first: bool = False) -> List[str]:
        executed_rules = []
        self.execution_log.clear()
        
        for rule in self.rules:
            if rule.evaluate(facts):
                try:
                    rule.execute(facts)
                    executed_rules.append(rule.name)
                    self.execution_log.append({
                        'rule': rule.name,
                        'status': 'success',
                        'facts': facts.copy()
                    })
                    
                    if stop_on_first:
                        break
                except Exception as e:
                    self.execution_log.append({
                        'rule': rule.name,
                        'status': 'error',
                        'error': str(e)
                    })
        
        return executed_rules
    
    def clear_rules(self) -> None:
        self.rules.clear()
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        return self.execution_log.copy()


class RuleBuilder:
    def __init__(self, name: str):
        self.name = name
        self.conditions: List[Condition] = []
        self.action: Optional[Callable] = None
        self.priority: int = 0
        self.all_conditions: bool = True
        self.description: str = ""
    
    def when(self, field: str, operator: Operator, value: Any) -> 'RuleBuilder':
        self.conditions.append(Condition(field, operator, value))
        return self
    
    def then(self, action: Callable[[Dict[str, Any]], None]) -> 'RuleBuilder':
        self.action = action
        return self
    
    def with_priority(self, priority: int) -> 'RuleBuilder':
        self.priority = priority
        return self
    
    def require_all(self) -> 'RuleBuilder':
        self.all_conditions = True
        return self
    
    def require_any(self) -> 'RuleBuilder':
        self.all_conditions = False
        return self
    
    def with_description(self, description: str) -> 'RuleBuilder':
        self.description = description
        return self
    
    def build(self) -> Rule:
        if not self.action:
            raise ValueError("Rule must have an action")
        
        return Rule(
            name=self.name,
            conditions=self.conditions,
            action=self.action,
            priority=self.priority,
            all_conditions=self.all_conditions,
            description=self.description
        )
