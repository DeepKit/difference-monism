import pytest
import sys
sys.path.insert(0, '.')
from workflow_engine import WorkflowEngine

def test_workflow_init():
    engine = WorkflowEngine()
    assert engine is not None

def test_workflow_add_node():
    engine = WorkflowEngine()
    engine.add_node("start", lambda: True)
    assert "start" in engine.nodes
