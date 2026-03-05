import pytest
import sys
sys.path.insert(0, '.')
from email_service import EmailService, EmailConfig

def test_email_init():
    config = EmailConfig(smtp_host="smtp.test.com", smtp_port=587, username="test", password="pass")
    service = EmailService(config)
    assert service is not None

def test_email_send():
    config = EmailConfig(smtp_host="smtp.test.com", smtp_port=587, username="test", password="pass")
    service = EmailService(config)
    # 不实际发送，只测试接口
    assert hasattr(service, 'send_email')