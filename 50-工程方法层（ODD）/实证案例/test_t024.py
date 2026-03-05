import pytest
import sys
sys.path.insert(0, '.')
from data_masker import DataMasker

def test_masker_init():
    masker = DataMasker()
    assert masker is not None

def test_mask_phone():
    masker = DataMasker()
    result = masker.mask_phone("13812345678")
    assert result == "138****5678"

def test_mask_email():
    masker = DataMasker()
    result = masker.mask_email("test@example.com")
    assert "@" in result and "example.com" in result

def test_mask_bank_card():
    masker = DataMasker()
    result = masker.mask_bank_card("6222021234567890")
    assert "6222" in result and "7890" in result
