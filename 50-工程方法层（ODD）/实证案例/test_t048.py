import pytest
import sys
sys.path.insert(0, '.')
from rules_engine import RulesEngine

def test_rules_init():
    engine = RulesEngine()
    assert engine is not None

def test_rules_add():
    engine = RulesEngine()
    engine.add_rule("rule1", lambda x: x > 0, lambda x: print("positive"))
    assert "rule1" in engine.rules

def test_rules_evaluate():
    engine = RulesEngine()
    engine.add_rule("rule1", lambda x: x > 0, lambda x: None)
    result = engine.evaluate(5)
    assert result == True
