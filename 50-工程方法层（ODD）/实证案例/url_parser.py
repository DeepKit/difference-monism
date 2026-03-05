from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Dict, Optional, List


class URLParser:
    def __init__(self, url: str):
        self.original_url = url
        self._parsed = urlparse(url)
        self._query_params = parse_qs(self._parsed.query, keep_blank_values=True)
    
    @property
    def scheme(self) -> str:
        """获取协议 (http, https, ftp等)"""
        return self._parsed.scheme
    
    @property
    def netloc(self) -> str:
        """获取网络位置 (域名:端口)"""
        return self._parsed.netloc
    
    @property
    def hostname(self) -> Optional[str]:
        """获取主机名"""
        return self._parsed.hostname
    
    @property
    def port(self) -> Optional[int]:
        """获取端口号"""
        return self._parsed.port
    
    @property
    def path(self) -> str:
        """获取路径"""
        return self._parsed.path
    
    @property
    def params(self) -> str:
        """获取参数"""
        return self._parsed.params
    
    @property
    def query(self) -> str:
        """获取查询字符串"""
        return self._parsed.query
    
    @property
    def fragment(self) -> str:
        """获取片段标识符"""
        return self._parsed.fragment
    
    @property
    def username(self) -> Optional[str]:
        """获取用户名"""
        return self._parsed.username
    
    @property
    def password(self) -> Optional[str]:
        """获取密码"""
        return self._parsed.password
    
    def get_query_param(self, key: str, default=None) -> Optional[str]:
        """获取单个查询参数"""
        values = self._query_params.get(key, [])
        return values[0] if values else default
    
    def get_query_params(self, key: str) -> List[str]:
        """获取查询参数列表"""
        return self._query_params.get(key, [])
    
    def get_all_query_params(self) -> Dict[str, List[str]]:
        """获取所有查询参数"""
        return self._query_params.copy()
    
    def set_query_param(self, key: str, value: str) -> 'URLParser':
        """设置查询参数"""
        self._query_params[key] = [value]
        return self
    
    def add_query_param(self, key: str, value: str) -> 'URLParser':
        """添加查询参数"""
        if key in self._query_params:
            self._query_params[key].append(value)
        else:
            self._query_params[key] = [value]
        return self
    
    def remove_query_param(self, key: str) -> 'URLParser':
        """删除查询参数"""
        self._query_params.pop(key, None)
        return self
    
    def build(self) -> str:
        """构建完整URL"""
        query_string = urlencode(self._query_params, doseq=True)
        return urlunparse((
            self.scheme,
            self.netloc,
            self.path,
            self.params,
            query_string,
            self.fragment
        ))
    
    def __str__(self) -> str:
        return self.build()
    
    def __repr__(self) -> str:
        return f"URLParser('{self.original_url}')"


# 使用示例
if __name__ == "__main__":
    url = "https://user:pass@example.com:8080/path/to/page?name=value&key=123#section"
    
    parser = URLParser(url)
    
    print(f"原始URL: {parser.original_url}")
    print(f"协议: {parser.scheme}")
    print(f"主机名: {parser.hostname}")
    print(f"端口: {parser.port}")
    print(f"路径: {parser.path}")
    print(f"查询字符串: {parser.query}")
    print(f"片段: {parser.fragment}")
    print(f"用户名: {parser.username}")
    print(f"密码: {parser.password}")
    print(f"查询参数: {parser.get_all_query_params()}")
    
    # 修改查询参数
    parser.set_query_param("name", "newvalue").add_query_param("extra", "data")
    print(f"修改后URL: {parser.build()}")