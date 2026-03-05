import random
import string


class RandomStringGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = string.punctuation
        self.all_chars = self.lowercase + self.uppercase + self.digits + self.special_chars
    
    def generate(self, length=10, use_lowercase=True, use_uppercase=True, 
                 use_digits=True, use_special=False):
        """生成随机字符串"""
        char_pool = ''
        if use_lowercase:
            char_pool += self.lowercase
        if use_uppercase:
            char_pool += self.uppercase
        if use_digits:
            char_pool += self.digits
        if use_special:
            char_pool += self.special_chars
        
        if not char_pool:
            raise ValueError("至少选择一种字符类型")
        
        return ''.join(random.choice(char_pool) for _ in range(length))
    
    def generate_alphanumeric(self, length=10):
        """生成字母数字混合字符串"""
        return self.generate(length, use_special=False)
    
    def generate_letters_only(self, length=10):
        """生成纯字母字符串"""
        return self.generate(length, use_digits=False, use_special=False)
    
    def generate_digits_only(self, length=10):
        """生成纯数字字符串"""
        return self.generate(length, use_lowercase=False, use_uppercase=False, 
                           use_digits=True, use_special=False)
    
    def generate_password(self, length=16):
        """生成强密码（包含所有字符类型）"""
        if length < 4:
            raise ValueError("密码长度至少为4")
        
        # 确保至少包含每种字符类型
        password = [
            random.choice(self.lowercase),
            random.choice(self.uppercase),
            random.choice(self.digits),
            random.choice(self.special_chars)
        ]
        
        # 填充剩余长度
        password += [random.choice(self.all_chars) for _ in range(length - 4)]
        
        # 打乱顺序
        random.shuffle(password)
        return ''.join(password)
    
    def generate_hex(self, length=10):
        """生成十六进制字符串"""
        return ''.join(random.choice('0123456789abcdef') for _ in range(length))
    
    def generate_custom(self, length=10, charset=None):
        """使用自定义字符集生成字符串"""
        if not charset:
            raise ValueError("必须提供字符集")
        return ''.join(random.choice(charset) for _ in range(length))


# 使用示例
if __name__ == "__main__":
    gen = RandomStringGenerator()
    
    print("随机字符串:", gen.generate(12))
    print("字母数字:", gen.generate_alphanumeric(10))
    print("纯字母:", gen.generate_letters_only(8))
    print("纯数字:", gen.generate_digits_only(6))
    print("强密码:", gen.generate_password(16))
    print("十六进制:", gen.generate_hex(8))
    print("自定义字符集:", gen.generate_custom(10, "ABC123"))