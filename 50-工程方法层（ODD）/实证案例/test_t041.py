import pytest
import sys
sys.path.insert(0, '.')
from jwt_token import JWTTokenManager

def test_jwt_init():
    jwt_mgr = JWTTokenManager(secret_key="test-secret-key")
    assert jwt_mgr is not None

def test_jwt_create_verify():
    jwt_mgr = JWTTokenManager(secret_key="test-secret-key")
    token = jwt_mgr.generate_access_token({"user_id": 123})
    assert token is not None
    
    payload = jwt_mgr.verify_token(token)
    assert payload is not None
    assert payload["user_id"] == 123
