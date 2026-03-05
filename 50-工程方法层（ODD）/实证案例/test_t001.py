import pytest
from user_registration import UserRegistry, RegistrationError


class TestUserRegistration:
    """用户注册功能测试"""
    
    def setup_method(self):
        """每个测试方法前创建新的注册实例"""
        self.registry = UserRegistry()
    
    # 邮箱格式验证测试
    def test_valid_email_registration(self):
        """测试有效邮箱格式"""
        result = self.registry.register("user@example.com", "password123")
        assert result["email"] == "user@example.com"
        assert result["status"] == "registered"
    
    def test_invalid_email_no_at_symbol(self):
        """测试无@符号的邮箱"""
        with pytest.raises(RegistrationError, match="邮箱格式不正确"):
            self.registry.register("userexample.com", "password123")
    
    def test_invalid_email_no_domain(self):
        """测试无域名的邮箱"""
        with pytest.raises(RegistrationError, match="邮箱格式不正确"):
            self.registry.register("user@", "password123")
    
    def test_invalid_email_no_tld(self):
        """测试无顶级域名的邮箱"""
        with pytest.raises(RegistrationError, match="邮箱格式不正确"):
            self.registry.register("user@example", "password123")
    
    def test_empty_email(self):
        """测试空邮箱"""
        with pytest.raises(RegistrationError, match="邮箱格式不正确"):
            self.registry.register("", "password123")
    
    # 重复注册测试（大小写不敏感）
    def test_duplicate_registration_same_case(self):
        """测试相同大小写的重复注册"""
        self.registry.register("user@example.com", "password123")
        with pytest.raises(RegistrationError, match="该邮箱已被注册"):
            self.registry.register("user@example.com", "password456")
    
    def test_duplicate_registration_different_case(self):
        """测试不同大小写的重复注册"""
        self.registry.register("User@Example.COM", "password123")
        with pytest.raises(RegistrationError, match="该邮箱已被注册"):
            self.registry.register("user@example.com", "password456")
    
    def test_duplicate_registration_mixed_case(self):
        """测试混合大小写的重复注册"""
        self.registry.register("user@example.com", "password123")
        with pytest.raises(RegistrationError, match="该邮箱已被注册"):
            self.registry.register("USER@EXAMPLE.COM", "password456")
    
    # 密码验证测试
    def test_valid_password_with_letters_and_digits(self):
        """测试有效密码（包含字母和数字）"""
        result = self.registry.register("user@example.com", "password123")
        assert result["status"] == "registered"
    
    def test_password_too_short(self):
        """测试密码长度不足8位"""
        with pytest.raises(RegistrationError, match="密码长度至少为8位"):
            self.registry.register("user@example.com", "pass123")
    
    def test_password_no_digits(self):
        """测试密码不包含数字"""
        with pytest.raises(RegistrationError, match="密码必须包含至少一个数字"):
            self.registry.register("user@example.com", "password")
    
    def test_password_no_letters(self):
        """测试密码不包含字母"""
        with pytest.raises(RegistrationError, match="密码必须包含至少一个字母"):
            self.registry.register("user@example.com", "12345678")
    
    def test_password_empty(self):
        """测试空密码"""
        with pytest.raises(RegistrationError, match="密码不能为空"):
            self.registry.register("user@example.com", "")
    
    def test_password_exactly_8_chars(self):
        """测试恰好8位的有效密码"""
        result = self.registry.register("user@example.com", "pass1234")
        assert result["status"] == "registered"
    
    def test_password_with_special_chars(self):
        """测试包含特殊字符的密码"""
        result = self.registry.register("user@example.com", "pass@123!")
        assert result["status"] == "registered"
    
    # 综合测试
    def test_multiple_users_registration(self):
        """测试多个用户注册"""
        self.registry.register("user1@example.com", "password123")
        self.registry.register("user2@example.com", "password456")
        self.registry.register("user3@example.com", "password789")
        
        assert self.registry.get_user_count() == 3
        assert self.registry.is_registered("user1@example.com")
        assert self.registry.is_registered("USER2@EXAMPLE.COM")
        assert not self.registry.is_registered("user4@example.com")
    
    def test_registration_preserves_original_email_case(self):
        """测试注册保留原始邮箱大小写"""
        result = self.registry.register("User@Example.COM", "password123")
        assert result["email"] == "User@Example.COM"


class TestEdgeCases:
    """边界情况测试"""
    
    def setup_method(self):
        self.registry = UserRegistry()
    
    def test_email_with_plus_sign(self):
        """测试包含+号的邮箱"""
        result = self.registry.register("user+tag@example.com", "password123")
        assert result["status"] == "registered"
    
    def test_email_with_dots(self):
        """测试包含多个点的邮箱"""
        result = self.registry.register("first.last@example.co.uk", "password123")
        assert result["status"] == "registered"
    
    def test_password_all_digits_except_one_letter(self):
        """测试几乎全是数字的密码"""
        result = self.registry.register("user@example.com", "1234567a")
        assert result["status"] == "registered"
    
    def test_password_all_letters_except_one_digit(self):
        """测试几乎全是字母的密码"""
        result = self.registry.register("user@example.com", "password1")
        assert result["status"] == "registered"
