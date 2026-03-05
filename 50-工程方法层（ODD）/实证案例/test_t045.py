import pytest
import sys
sys.path.insert(0, '.')
from xss_filter import XSSFilter

def test_xss_init():
    f = XSSFilter()
    assert f is not None

def test_xss_filter():
    f = XSSFilter()
    result = f.filter("<script>alert('xss')</script>")
    assert "<script>" not in result

def test_xss_filter_html():
    f = XSSFilter()
    result = f.filter("<b>hello</b>")
    assert "hello" in result
