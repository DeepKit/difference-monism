import time
import hashlib
import json
import threading
from typing import Any, Dict, Optional, Tuple, Callable
from collections import OrderedDict
from datetime import datetime, timedelta
import requests
from requests.exceptions import RequestException


class APICacheProxy:
    """API缓存代理类，支持LRU缓存、TTL过期、线程安全"""
    
    def __init__(
        self,
        max_size: int = 1000,
        default_ttl: int = 300,
        enable_cache: bool = True
    ):
        """
        初始化API缓存代理
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认缓存过期时间（秒）
            enable_cache: 是否启用缓存
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.enable_cache = enable_cache
        self._cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self._lock = threading.RLock()
        self._stats = {
            'hits': 0,
            'misses': 0,
            'errors': 0,
            'total_requests': 0
        }
    
    def _generate_cache_key(
        self,
        url: str,
        method: str = 'GET',
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> str:
        """生成缓存键"""
        key_parts = [method.upper(), url]
        
        if params:
            key_parts.append(json.dumps(params, sort_keys=True))
        if data:
            key_parts.append(json.dumps(data, sort_keys=True))
        if headers:
            # 只包含影响响应的关键头
            relevant_headers = {k: v for k, v in headers.items() 
                              if k.lower() in ['authorization', 'content-type', 'accept']}
            if relevant_headers:
                key_parts.append(json.dumps(relevant_headers, sort_keys=True))
        
        key_string = '|'.join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def _is_expired(self, timestamp: float, ttl: int) -> bool:
        """检查缓存是否过期"""
        return time.time() - timestamp > ttl
    
    def _evict_if_needed(self):
        """如果超过最大容量，移除最旧的条目"""
        while len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)
    
    def _get_from_cache(self, cache_key: str, ttl: int) -> Optional[Any]:
        """从缓存获取数据"""
        with self._lock:
            if cache_key in self._cache:
                data, timestamp = self._cache[cache_key]
                if not self._is_expired(timestamp, ttl):
                    # 移到末尾（LRU）
                    self._cache.move_to_end(cache_key)
                    self._stats['hits'] += 1
                    return data
                else:
                    # 过期，删除
                    del self._cache[cache_key]
            
            self._stats['misses'] += 1
            return None
    
    def _set_to_cache(self, cache_key: str, data: Any):
        """设置缓存数据"""
        with self._lock:
            self._evict_if_needed()
            self._cache[cache_key] = (data, time.time())
            self._cache.move_to_end(cache_key)
    
    def request(
        self,
        url: str,
        method: str = 'GET',
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: int = 30,
        ttl: Optional[int] = None,
        force_refresh: bool = False,
        **kwargs
    ) -> requests.Response:
        """
        发送HTTP请求，支持缓存
        
        Args:
            url: 请求URL
            method: HTTP方法
            params: URL参数
            data: 表单数据
            json_data: JSON数据
            headers: 请求头
            timeout: 超时时间
            ttl: 缓存过期时间（秒），None使用默认值
            force_refresh: 强制刷新缓存
            **kwargs: 其他requests参数
            
        Returns:
            requests.Response对象
            
        Raises:
            RequestException: 请求失败
        """
        self._stats['total_requests'] += 1
        ttl = ttl if ttl is not None else self.default_ttl
        
        # 生成缓存键
        cache_key = self._generate_cache_key(
            url, method, params, data or json_data, headers
        )
        
        # 检查缓存
        if self.enable_cache and not force_refresh and method.upper() == 'GET':
            cached_response = self._get_from_cache(cache_key, ttl)
            if cached_response is not None:
                return cached_response
        
        # 发送实际请求
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout,
                **kwargs
            )
            response.raise_for_status()
            
            # 缓存成功的GET请求
            if self.enable_cache and method.upper() == 'GET':
                self._set_to_cache(cache_key, response)
            
            return response
            
        except RequestException as e:
            self._stats['errors'] += 1
            raise
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """GET请求"""
        return self.request(url, method='GET', **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """POST请求"""
        return self.request(url, method='POST', **kwargs)
    
    def put(self, url: str, **kwargs) -> requests.Response:
        """PUT请求"""
        return self.request(url, method='PUT', **kwargs)
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        """DELETE请求"""
        return self.request(url, method='DELETE', **kwargs)
    
    def clear_cache(self):
        """清空所有缓存"""
        with self._lock:
            self._cache.clear()
    
    def invalidate(
        self,
        url: str,
        method: str = 'GET',
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ):
        """使特定缓存失效"""
        cache_key = self._generate_cache_key(url, method, params, data, headers)
        with self._lock:
            if cache_key in self._cache:
                del self._cache[cache_key]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self._lock:
            hit_rate = (
                self._stats['hits'] / (self._stats['hits'] + self._stats['misses'])
                if (self._stats['hits'] + self._stats['misses']) > 0
                else 0
            )
            return {
                **self._stats,
                'cache_size': len(self._cache),
                'hit_rate': f"{hit_rate:.2%}",
                'max_size': self.max_size
            }
    
    def set_cache_enabled(self, enabled: bool):
        """启用或禁用缓存"""
        self.enable_cache = enabled
        if not enabled:
            self.clear_cache()


# 使用示例
if __name__ == '__main__':
    # 创建代理实例
    proxy = APICacheProxy(max_size=500, default_ttl=60)
    
    try:
        # 第一次请求（缓存未命中）
        response1 = proxy.get('https://api.github.com/users/github')
        print(f"状态码: {response1.status_code}")
        print(f"第一次请求统计: {proxy.get_stats()}")
        
        # 第二次请求（缓存命中）
        response2 = proxy.get('https://api.github.com/users/github')
        print(f"第二次请求统计: {proxy.get_stats()}")
        
        # 强制刷新
        response3 = proxy.get('https://api.github.com/users/github', force_refresh=True)
        print(f"强制刷新后统计: {proxy.get_stats()}")
        
        # POST请求（不缓存）
        # response4 = proxy.post('https://api.example.com/data', json_data={'key': 'value'})
        
        # 清空缓存
        proxy.clear_cache()
        print(f"清空后缓存大小: {proxy.get_stats()['cache_size']}")
        
    except RequestException as e:
        print(f"请求错误: {e}")