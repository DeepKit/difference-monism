from typing import Any, Dict, List, Union, Optional
from enum import Enum
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import base64


class MessageFormat(Enum):
    JSON = "json"
    XML = "xml"
    DICT = "dict"
    STRING = "string"


class MessageConverter:
    """消息格式转换类"""
    
    def __init__(self):
        self.encoding = 'utf-8'
    
    def to_json(self, data: Any, pretty: bool = False) -> str:
        """转换为JSON格式"""
        indent = 4 if pretty else None
        return json.dumps(data, ensure_ascii=False, indent=indent, default=str)
    
    def from_json(self, json_str: str) -> Any:
        """从JSON字符串解析"""
        return json.loads(json_str)
    
    def to_xml(self, data: Dict, root_tag: str = "message") -> str:
        """转换为XML格式"""
        root = ET.Element(root_tag)
        self._dict_to_xml(root, data)
        return ET.tostring(root, encoding='unicode')
    
    def from_xml(self, xml_str: str) -> Dict:
        """从XML字符串解析"""
        root = ET.fromstring(xml_str)
        return self._xml_to_dict(root)
    
    def _dict_to_xml(self, parent: ET.Element, data: Union[Dict, List, Any]):
        """递归转换字典到XML"""
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, str(key))
                self._dict_to_xml(child, value)
        elif isinstance(data, list):
            for item in data:
                child = ET.SubElement(parent, "item")
                self._dict_to_xml(child, item)
        else:
            parent.text = str(data)
    
    def _xml_to_dict(self, element: ET.Element) -> Union[Dict, str]:
        """递归转换XML到字典"""
        result = {}
        
        if len(element) == 0:
            return element.text or ""
        
        for child in element:
            child_data = self._xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result
    
    def convert(self, data: Any, from_format: MessageFormat, 
                to_format: MessageFormat) -> Any:
        """通用格式转换"""
        # 先转换为字典格式
        if from_format == MessageFormat.JSON:
            intermediate = self.from_json(data)
        elif from_format == MessageFormat.XML:
            intermediate = self.from_xml(data)
        elif from_format == MessageFormat.STRING:
            intermediate = {"content": data}
        else:
            intermediate = data
        
        # 再转换为目标格式
        if to_format == MessageFormat.JSON:
            return self.to_json(intermediate)
        elif to_format == MessageFormat.XML:
            return self.to_xml(intermediate)
        elif to_format == MessageFormat.STRING:
            return str(intermediate)
        else:
            return intermediate
    
    def encode_base64(self, data: Union[str, bytes]) -> str:
        """Base64编码"""
        if isinstance(data, str):
            data = data.encode(self.encoding)
        return base64.b64encode(data).decode('ascii')
    
    def decode_base64(self, encoded: str) -> str:
        """Base64解码"""
        return base64.b64decode(encoded).decode(self.encoding)
    
    def normalize_message(self, message: Dict) -> Dict:
        """标准化消息格式"""
        return {
            "id": message.get("id", ""),
            "timestamp": message.get("timestamp", datetime.now().isoformat()),
            "type": message.get("type", "unknown"),
            "content": message.get("content", {}),
            "metadata": message.get("metadata", {})
        }
    
    def batch_convert(self, messages: List[Any], from_format: MessageFormat,
                     to_format: MessageFormat) -> List[Any]:
        """批量转换消息"""
        return [self.convert(msg, from_format, to_format) for msg in messages]


# 使用示例
if __name__ == "__main__":
    converter = MessageConverter()
    
    # 示例数据
    data = {
        "user": "张三",
        "message": "你好",
        "timestamp": "2024-01-01T12:00:00"
    }
    
    # 转JSON
    json_str = converter.to_json(data, pretty=True)
    print("JSON:", json_str)
    
    # 转XML
    xml_str = converter.to_xml(data)
    print("\nXML:", xml_str)
    
    # JSON到XML
    result = converter.convert(json_str, MessageFormat.JSON, MessageFormat.XML)
    print("\nJSON->XML:", result)
    
    # Base64编码
    encoded = converter.encode_base64("测试消息")
    print("\nBase64:", encoded)
    print("解码:", converter.decode_base64(encoded))