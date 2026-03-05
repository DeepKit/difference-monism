from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class TargetInterface(ABC):
    """目标接口"""
    
    @abstractmethod
    def request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class Adaptee:
    """需要被适配的类"""
    
    def specific_request(self, old_format_data: str) -> str:
        return f"Adaptee处理: {old_format_data}"


class AdapterV2(TargetInterface):
    """适配器V2实现"""
    
    def __init__(self, adaptee: Adaptee):
        self._adaptee = adaptee
        self._cache: Dict[str, Any] = {}
    
    def request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """适配新接口到旧接口"""
        # 数据转换
        old_format = self._convert_to_old_format(data)
        
        # 调用旧接口
        result = self._adaptee.specific_request(old_format)
        
        # 结果转换
        return self._convert_to_new_format(result)
    
    def _convert_to_old_format(self, data: Dict[str, Any]) -> str:
        """转换为旧格式"""
        return str(data.get('payload', ''))
    
    def _convert_to_new_format(self, result: str) -> Dict[str, Any]:
        """转换为新格式"""
        return {
            'status': 'success',
            'data': result,
            'version': 'v2'
        }
    
    def clear_cache(self) -> None:
        """清除缓存"""
        self._cache.clear()


# 使用示例
if __name__ == '__main__':
    adaptee = Adaptee()
    adapter = AdapterV2(adaptee)
    
    request_data = {'payload': 'test data'}
    response = adapter.request(request_data)
    print(response)