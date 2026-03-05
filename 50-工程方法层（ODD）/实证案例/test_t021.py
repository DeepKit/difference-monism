import pytest
import sys
sys.path.insert(0, '.')
from csv_exporter import CSVExporter
import tempfile
import os

def test_csv_exporter():
    exporter = CSVExporter()
    data = [{"name": "Alice", "age": 30}]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        tmpfile = f.name
    try:
        result = exporter.export_to_file(data, tmpfile)
        assert result == True
    finally:
        if os.path.exists(tmpfile):
            os.remove(tmpfile)