import pytest
import sys
sys.path.insert(0, '.')
from api_signature import APISignatureValidator

def test_signature_init():
    v = APISignatureValidator(secret_key="test-key")
    assert v is not None

def test_signature_sign():
    v = APISignatureValidator(secret_key="test-key")
    sig = v.sign({"name": "test"})
    assert sig is not None

def test_signature_verify():
    v = APISignatureValidator(secret_key="test-key")
    params = {"name": "test"}
    sig = v.sign(params)
    result = v.verify(params, sig)
    assert result == True
