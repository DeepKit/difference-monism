import random
import string


class RandomStringGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.letters = string.ascii_letters
        self.alphanumeric = string.ascii_letters + string.digits
        self.punctuation = string.punctuation
    
    def generate(self, length=8, charset=None):
        """生成随机字符串"""
        if charset is None:
            charset = self.alphanumeric
        return ''.join(random.choice(charset) for _ in range(length))
    
    def alphanumeric(self, length=8):
        """生成字母数字混合字符串"""
        return self.generate(length, self.alphanumeric)
    
    def letters_only(self, length=8):
        """生成纯字母字符串"""
        return self.generate(length, self.letters)
    
    def digits_only(self, length=8):
        """生成纯数字字符串"""
        return self.generate(length, self.digits)
    
    def lowercase_only(self, length=8):
        """生成小写字母字符串"""
        return self.generate(length, self.lowercase)
    
    def uppercase_only(self, length=8):
        """生成大写字母字符串"""
        return self.generate(length, self.uppercase)
    
    def with_special(self, length=8):
        """生成包含特殊字符的字符串"""
        charset = self.alphanumeric + self.punctuation
        return self.generate(length, charset)


# 使用示例
if __name__ == "__main__":
    gen = RandomStringGenerator()
    
    print(gen.generate(10))              # 默认字母数字混合
    print(gen.letters_only(12))          # 纯字母
    print(gen.digits_only(6))            # 纯数字
    print(gen.with_special(15))          # 包含特殊字符
    print(gen.generate(8, "ABC123"))     # 自定义字符集