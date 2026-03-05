import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from urllib.parse import urlparse


class Cookie:
    """单个Cookie对象"""
    
    def __init__(self, name: str, value: str, **kwargs):
        self.name = name
        self.value = value
        self.domain = kwargs.get('domain', '')
        self.path = kwargs.get('path', '/')
        self.expires = kwargs.get('expires')
        self.max_age = kwargs.get('max_age')
        self.secure = kwargs.get('secure', False)
        self.httponly = kwargs.get('httponly', False)
        self.samesite = kwargs.get('samesite', 'Lax')
        self.created_at = time.time()
    
    def is_expired(self) -> bool:
        """检查Cookie是否过期"""
        if self.max_age is not None:
            return time.time() - self.created_at > self.max_age
        
        if self.expires:
            if isinstance(self.expires, str):
                try:
                    expires_time = datetime.strptime(
                        self.expires, '%a, %d %b %Y %H:%M:%S GMT'
                    )
                    return datetime.utcnow() > expires_time
                except ValueError:
                    return False
            elif isinstance(self.expires, datetime):
                return datetime.utcnow() > self.expires
        
        return False
    
    def matches_domain(self, domain: str) -> bool:
        """检查Cookie是否匹配指定域名"""
        if not self.domain:
            return True
        
        domain = domain.lower()
        cookie_domain = self.domain.lower()
        
        if cookie_domain.startswith('.'):
            return domain.endswith(cookie_domain) or domain == cookie_domain[1:]
        
        return domain == cookie_domain
    
    def matches_path(self, path: str) -> bool:
        """检查Cookie是否匹配指定路径"""
        if not self.path:
            return True
        return path.startswith(self.path)
    
    def to_header(self) -> str:
        """转换为HTTP头格式"""
        return f"{self.name}={self.value}"
    
    def to_set_cookie_header(self) -> str:
        """转换为Set-Cookie头格式"""
        parts = [f"{self.name}={self.value}"]
        
        if self.domain:
            parts.append(f"Domain={self.domain}")
        if self.path:
            parts.append(f"Path={self.path}")
        if self.expires:
            if isinstance(self.expires, datetime):
                expires_str = self.expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
            else:
                expires_str = self.expires
            parts.append(f"Expires={expires_str}")
        if self.max_age is not None:
            parts.append(f"Max-Age={self.max_age}")
        if self.secure:
            parts.append("Secure")
        if self.httponly:
            parts.append("HttpOnly")
        if self.samesite:
            parts.append(f"SameSite={self.samesite}")
        
        return "; ".join(parts)
    
    def __repr__(self):
        return f"Cookie(name={self.name}, value={self.value}, domain={self.domain})"


class CookieJar:
    """Cookie管理器"""
    
    def __init__(self):
        self.cookies: Dict[str, Cookie] = {}
    
    def set(self, name: str, value: str, **kwargs) -> None:
        """设置Cookie"""
        cookie = Cookie(name, value, **kwargs)
        key = self._make_key(name, kwargs.get('domain', ''), kwargs.get('path', '/'))
        self.cookies[key] = cookie
    
    def get(self, name: str, domain: str = '', path: str = '/') -> Optional[Cookie]:
        """获取Cookie"""
        key = self._make_key(name, domain, path)
        cookie = self.cookies.get(key)
        
        if cookie and cookie.is_expired():
            del self.cookies[key]
            return None
        
        return cookie
    
    def delete(self, name: str, domain: str = '', path: str = '/') -> None:
        """删除Cookie"""
        key = self._make_key(name, domain, path)
        self.cookies.pop(key, None)
    
    def clear(self) -> None:
        """清空所有Cookie"""
        self.cookies.clear()
    
    def clear_expired(self) -> None:
        """清除过期的Cookie"""
        expired_keys = [
            key for key, cookie in self.cookies.items()
            if cookie.is_expired()
        ]
        for key in expired_keys:
            del self.cookies[key]
    
    def get_cookies_for_url(self, url: str) -> List[Cookie]:
        """获取适用于指定URL的所有Cookie"""
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path or '/'
        is_secure = parsed.scheme == 'https'
        
        self.clear_expired()
        
        matching_cookies = []
        for cookie in self.cookies.values():
            if cookie.matches_domain(domain) and cookie.matches_path(path):
                if not cookie.secure or is_secure:
                    matching_cookies.append(cookie)
        
        return matching_cookies
    
    def get_cookie_header(self, url: str) -> str:
        """获取适用于指定URL的Cookie头"""
        cookies = self.get_cookies_for_url(url)
        return "; ".join(cookie.to_header() for cookie in cookies)
    
    def parse_set_cookie(self, set_cookie_header: str, url: str = '') -> None:
        """解析Set-Cookie头"""
        parts = [part.strip() for part in set_cookie_header.split(';')]
        
        if not parts:
            return
        
        name_value = parts[0].split('=', 1)
        if len(name_value) != 2:
            return
        
        name, value = name_value
        attributes = {}
        
        for part in parts[1:]:
            if '=' in part:
                attr_name, attr_value = part.split('=', 1)
                attr_name = attr_name.strip().lower()
                attr_value = attr_value.strip()
                
                if attr_name == 'domain':
                    attributes['domain'] = attr_value
                elif attr_name == 'path':
                    attributes['path'] = attr_value
                elif attr_name == 'expires':
                    attributes['expires'] = attr_value
                elif attr_name == 'max-age':
                    try:
                        attributes['max_age'] = int(attr_value)
                    except ValueError:
                        pass
                elif attr_name == 'samesite':
                    attributes['samesite'] = attr_value
            else:
                attr = part.strip().lower()
                if attr == 'secure':
                    attributes['secure'] = True
                elif attr == 'httponly':
                    attributes['httponly'] = True
        
        if url and 'domain' not in attributes:
            parsed = urlparse(url)
            attributes['domain'] = parsed.netloc
        
        self.set(name, value, **attributes)
    
    def parse_cookie_header(self, cookie_header: str, domain: str = '', path: str = '/') -> None:
        """解析Cookie头"""
        for cookie_str in cookie_header.split(';'):
            cookie_str = cookie_str.strip()
            if '=' in cookie_str:
                name, value = cookie_str.split('=', 1)
                self.set(name.strip(), value.strip(), domain=domain, path=path)
    
    def _make_key(self, name: str, domain: str, path: str) -> str:
        """生成Cookie的唯一键"""
        return f"{name}|{domain}|{path}"
    
    def __len__(self):
        return len(self.cookies)
    
    def __repr__(self):
        return f"CookieJar(cookies={len(self.cookies)})"


# 使用示例
if __name__ == "__main__":
    jar = CookieJar()
    
    # 设置Cookie
    jar.set('session_id', 'abc123', domain='example.com', path='/', max_age=3600)
    jar.set('user', 'john', domain='example.com', secure=True, httponly=True)
    
    # 解析Set-Cookie头
    jar.parse_set_cookie('token=xyz789; Domain=example.com; Path=/; Secure; HttpOnly')
    
    # 获取Cookie
    cookie = jar.get('session_id', 'example.com', '/')
    print(f"Cookie: {cookie}")
    
    # 获取URL的Cookie头
    header = jar.get_cookie_header('https://example.com/api')
    print(f"Cookie Header: {header}")
    
    # 清除过期Cookie
    jar.clear_expired()
    
    print(f"Total cookies: {len(jar)}")