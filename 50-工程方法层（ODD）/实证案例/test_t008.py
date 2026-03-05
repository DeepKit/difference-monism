import pytest
import time
from sms_verification import SMSVerificationService


@pytest.fixture
def service():
    return SMSVerificationService()


class TestSendCode:
    def test_send_code_success(self, service):
        success, message = service.send_code("13800138000")
        assert success is True
        assert "验证码已发送" in message
        record = service.get_record("13800138000")
        assert record is not None
        assert len(record.code) == 6
        assert record.code.isdigit()
    
    def test_send_code_rate_limit(self, service):
        phone = "13800138001"
        success, _ = service.send_code(phone)
        assert success is True
        success, message = service.send_code(phone)
        assert success is False
        assert "发送过于频繁" in message
    
    def test_send_code_after_interval(self, service):
        phone = "13800138002"
        service.send_code(phone)
        first_code = service.get_record(phone).code
        service.last_send_time[phone] -= 61
        success, _ = service.send_code(phone)
        assert success is True
        second_code = service.get_record(phone).code
        assert first_code != second_code
    
    def test_send_code_when_locked(self, service):
        phone = "13800138003"
        service.send_code(phone)
        record = service.get_record(phone)
        record.locked_until = time.time() + 100
        success, message = service.send_code(phone)
        assert success is False
        assert "账号已锁定" in message


class TestVerifyCode:
    def test_verify_code_success(self, service):
        phone = "13800138010"
        service.send_code(phone)
        code = service.get_record(phone).code
        success, message = service.verify_code(phone, code)
        assert success is True
        assert "验证成功" in message
        assert service.get_record(phone) is None
    
    def test_verify_code_not_exist(self, service):
        success, message = service.verify_code("13800138011", "123456")
        assert success is False
        assert "请先获取验证码" in message
    
    def test_verify_code_expired(self, service):
        phone = "13800138012"
        service.send_code(phone)
        record = service.get_record(phone)
        record.expires_at = time.time() - 1
        success, message = service.verify_code(phone, record.code)
        assert success is False
        assert "验证码已过期" in message
    
    def test_verify_code_wrong(self, service):
        phone = "13800138013"
        service.send_code(phone)
        correct_code = service.get_record(phone).code
        wrong_code = "000000" if correct_code != "000000" else "111111"
        success, message = service.verify_code(phone, wrong_code)
        assert success is False
        assert "验证码错误" in message
        assert "还有2次机会" in message
    
    def test_verify_code_max_errors(self, service):
        phone = "13800138014"
        service.send_code(phone)
        wrong_code = "000000"
        for i in range(2):
            success, message = service.verify_code(phone, wrong_code)
            assert success is False
        success, message = service.verify_code(phone, wrong_code)
        assert success is False
        assert "账号已锁定" in message
        record = service.get_record(phone)
        assert record.locked_until is not None
    
    def test_verify_code_locked(self, service):
        phone = "13800138015"
        service.send_code(phone)
        record = service.get_record(phone)
        record.locked_until = time.time() + 100
        success, message = service.verify_code(phone, record.code)
        assert success is False
        assert "账号已锁定" in message
    
    def test_verify_code_invalidates_after_success(self, service):
        phone = "13800138016"
        service.send_code(phone)
        code = service.get_record(phone).code
        success, _ = service.verify_code(phone, code)
        assert success is True
        success, message = service.verify_code(phone, code)
        assert success is False
        assert "请先获取验证码" in message


class TestEdgeCases:
    def test_multiple_phones(self, service):
        phone1 = "13800138020"
        phone2 = "13800138021"
        service.send_code(phone1)
        service.send_code(phone2)
        code1 = service.get_record(phone1).code
        code2 = service.get_record(phone2).code
        assert code1 != code2
        service.verify_code(phone1, "000000")
        record2 = service.get_record(phone2)
        assert record2.error_count == 0
    
    def test_code_generation_randomness(self, service):
        codes = set()
        for i in range(100):
            phone = f"1380013{i:04d}"
            service.send_code(phone)
            codes.add(service.get_record(phone).code)
        assert len(codes) > 90
