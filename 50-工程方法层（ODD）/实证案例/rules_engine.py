
from typing import Any, Callable, Dict, List, Union
from dataclasses import dataclass
from enum import Enum


class Operator(Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"


@dataclass
class Condition:
    field: str
    operator: Operator
    value: Any
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        field_value = context.get(self.field)
        
        if self.operator == Operator.EQUALS:
            return field_value == self.value
        elif self.operator == Operator.NOT_EQUALS:
            return field_value != self.value
        elif self.operator == Operator.GREATER_THAN:
            return field_value > self.value
        elif self.operator == Operator.LESS_THAN:
            return field_value < self.value
        elif self.operator == Operator.GREATER_EQUAL:
            return field_value >= self.value
        elif self.operator == Operator.LESS_EQUAL:
            return field_value <= self.value
        elif self.operator == Operator.IN:
            return field_value in self.value
        elif self.operator == Operator.NOT_IN:
            return field_value not in self.value
        elif self.operator == Operator.CONTAINS:
            return self.value in field_value
        elif self.operator == Operator.STARTS_WITH:
            return str(field_value).startswith(str(self.value))
        elif self.operator == Operator.ENDS_WITH:
            return str(field_value).endswith(str(self.value))
        return False


@dataclass
class Rule:
    name: str
    conditions: List[Condition]
    actions: List[Callable]
    match_all: bool = True
    priority: int = 0
    
    def matches(self, context: Dict[str, Any]) -> bool:
        if not self.conditions:
            return True
        
        if self.match_all:
            return all(condition.evaluate(context) for condition in self.conditions)
        else:
            return any(condition.evaluate(context) for condition in self.conditions)
    
    def execute(self, context: Dict[str, Any]) -> List[Any]:
        results = []
        for action in self.actions:
            result = action(context)
            results.append(result)
        return results


class RulesEngine:
    def __init__(self):
        self.rules: List[Rule] = []
    
    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def remove_rule(self, rule_name: str) -> bool:
        initial_length = len(self.rules)
        self.rules = [r for r in self.rules if r.name != rule_name]
        return len(self.rules) < initial_length
    
    def get_rule(self, rule_name: str) -> Union[Rule, None]:
        for rule in self.rules:
            if rule.name == rule_name:
                return rule
        return None
    
    def evaluate(self, context: Dict[str, Any], stop_on_first: bool = False) -> Dict[str, List[Any]]:
        results = {}
        
        for rule in self.rules:
            if rule.matches(context):
                results[rule.name] = rule.execute(context)
                if stop_on_first:
                    break
        
        return results
    
    def clear_rules(self) -> None:
        self.rules.clear()


# Example usage
if __name__ == "__main__":
    engine = RulesEngine()
    
    # Define actions
    def send_email(context):
        return f"Email sent to {context.get('email')}"
    
    def apply_discount(context):
        price = context.get('price', 0)
        discount = price * 0.1
        return f"Discount applied: ${discount}"
    
    def log_event(context):
        return f"Event logged: {context.get('event_type')}"
    
    # Create rules
    vip_rule = Rule(
        name="VIP Customer Rule",
        conditions=[
            Condition("customer_type", Operator.EQUALS, "VIP"),
            Condition("purchase_amount", Operator.GREATER_THAN, 100)
        ],
        actions=[send_email, apply_discount],
        priority=10
    )
    
    new_customer_rule = Rule(
        name="New Customer Rule",
        conditions=[
            Condition("customer_type", Operator.EQUALS, "NEW")
        ],
        actions=[send_email, log_event],
        priority=5
    )
    
    # Add rules to engine
    engine.add_rule(vip_rule)
    engine.add_rule(new_customer_rule)
    
    # Test context
    context = {
        "customer_type": "VIP",
        "purchase_amount": 150,
        "email": "customer@example.com",
        "price": 200
    }
    
    # Execute rules
    results = engine.evaluate(context)
    
    for rule_name, actions_results in results.items():
        print(f"\n{rule_name}:")
        for result in actions_results:
            print(f"  - {result}")
