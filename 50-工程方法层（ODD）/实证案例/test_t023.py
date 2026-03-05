import pytest
import sys
sys.path.insert(0, '.')
from json_validator import JSONValidator

def test_validator_init():
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    v = JSONValidator(schema)
    assert v is not None

def test_validator_valid():
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    v = JSONValidator(schema)
    result = v.validate({"name": "test"})
    assert result == True

def test_validator_invalid():
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    v = JSONValidator(schema)
    result = v.validate({"name": 123})
    assert result == False