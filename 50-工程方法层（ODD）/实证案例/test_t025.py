import pytest
import sys
sys.path.insert(0, '.')
from data_encryptor import DataEncryptor

def test_encryptor_init():
    enc = DataEncryptor()
    assert enc is not None
    assert enc.key is not None

def test_encrypt_decrypt():
    enc = DataEncryptor()
    encrypted = enc.encrypt("hello world")
    assert 'ciphertext' in encrypted
    
    decrypted = enc.decrypt(encrypted)
    assert decrypted == b"hello world"

def test_encrypt_string():
    enc = DataEncryptor()
    result = enc.encrypt_string("test data")
    assert 'ciphertext' in result