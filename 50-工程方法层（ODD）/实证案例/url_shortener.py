import hashlib
import string
import random


class URLShortener:
    def __init__(self, base_url="http://short.url/"):
        self.url_map = {}  # short_code -> original_url
        self.reverse_map = {}  # original_url -> short_code
        self.base_url = base_url
        self.counter = 0
        
    def shorten(self, original_url):
        """将长URL转换为短URL"""
        if original_url in self.reverse_map:
            return self.base_url + self.reverse_map[original_url]
        
        short_code = self._generate_short_code(original_url)
        self.url_map[short_code] = original_url
        self.reverse_map[original_url] = short_code
        
        return self.base_url + short_code
    
    def expand(self, short_url):
        """将短URL还原为原始URL"""
        short_code = short_url.replace(self.base_url, "")
        return self.url_map.get(short_code)
    
    def _generate_short_code(self, url, length=6):
        """生成短码"""
        # 方法1: 使用计数器 + base62编码
        self.counter += 1
        return self._base62_encode(self.counter)
    
    def _base62_encode(self, num):
        """Base62编码"""
        chars = string.ascii_letters + string.digits
        if num == 0:
            return chars[0]
        
        result = []
        while num > 0:
            result.append(chars[num % 62])
            num //= 62
        
        return ''.join(reversed(result))


# 使用示例
if __name__ == "__main__":
    shortener = URLShortener()
    
    # 缩短URL
    long_url = "https://www.example.com/very/long/path/to/resource"
    short_url = shortener.shorten(long_url)
    print(f"短链接: {short_url}")
    
    # 还原URL
    original = shortener.expand(short_url)
    print(f"原始链接: {original}")
    
    # 测试多个URL
    urls = [
        "https://github.com/user/repo",
        "https://stackoverflow.com/questions/12345",
        "https://www.example.com/very/long/path/to/resource"
    ]
    
    for url in urls:
        short = shortener.shorten(url)
        print(f"{url} -> {short}")