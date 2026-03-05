import hashlib
from typing import Dict, Optional


class URLShortener:
    def __init__(self, base_url: str = "http://short.url/"):
        self.base_url = base_url
        self.url_map: Dict[str, str] = {}
        self.reverse_map: Dict[str, str] = {}
        self.counter = 0
    
    def _encode(self, num: int) -> str:
        """将数字编码为base62字符串"""
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num == 0:
            return chars[0]
        
        result = []
        while num:
            result.append(chars[num % 62])
            num //= 62
        return ''.join(reversed(result))
    
    def shorten(self, long_url: str) -> str:
        """缩短URL"""
        if long_url in self.reverse_map:
            return self.base_url + self.reverse_map[long_url]
        
        short_code = self._encode(self.counter)
        self.counter += 1
        
        self.url_map[short_code] = long_url
        self.reverse_map[long_url] = short_code
        
        return self.base_url + short_code
    
    def expand(self, short_url: str) -> Optional[str]:
        """还原URL"""
        short_code = short_url.replace(self.base_url, "")
        return self.url_map.get(short_code)


# 使用示例
if __name__ == "__main__":
    shortener = URLShortener()
    
    # 缩短URL
    short1 = shortener.shorten("https://www.example.com/very/long/url/path")
    print(f"短链接: {short1}")
    
    # 还原URL
    original = shortener.expand(short1)
    print(f"原始URL: {original}")
    
    # 相同URL返回相同短链接
    short2 = shortener.shorten("https://www.example.com/very/long/url/path")
    print(f"相同URL: {short1 == short2}")