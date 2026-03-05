import xml.etree.ElementTree as ET
from typing import Optional, List, Dict, Any
from io import StringIO


class XMLParser:
    """XML解析器类"""
    
    def __init__(self, xml_string: Optional[str] = None, xml_file: Optional[str] = None):
        """
        初始化XML解析器
        :param xml_string: XML字符串
        :param xml_file: XML文件路径
        """
        self.root = None
        self.tree = None
        
        if xml_string:
            self.parse_string(xml_string)
        elif xml_file:
            self.parse_file(xml_file)
    
    def parse_string(self, xml_string: str):
        """解析XML字符串"""
        self.root = ET.fromstring(xml_string)
        self.tree = ET.ElementTree(self.root)
        return self
    
    def parse_file(self, file_path: str):
        """解析XML文件"""
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        return self
    
    def get_root(self) -> ET.Element:
        """获取根元素"""
        return self.root
    
    def find(self, path: str) -> Optional[ET.Element]:
        """查找单个元素"""
        return self.root.find(path) if self.root is not None else None
    
    def findall(self, path: str) -> List[ET.Element]:
        """查找所有匹配的元素"""
        return self.root.findall(path) if self.root is not None else []
    
    def get_text(self, path: str, default: str = "") -> str:
        """获取元素文本内容"""
        element = self.find(path)
        return element.text if element is not None and element.text else default
    
    def get_attribute(self, path: str, attr_name: str, default: Any = None) -> Any:
        """获取元素属性值"""
        element = self.find(path)
        return element.get(attr_name, default) if element is not None else default
    
    def get_all_attributes(self, path: str) -> Dict[str, str]:
        """获取元素所有属性"""
        element = self.find(path)
        return element.attrib if element is not None else {}
    
    def to_dict(self, element: Optional[ET.Element] = None) -> Dict:
        """将XML转换为字典"""
        if element is None:
            element = self.root
        
        result = {
            'tag': element.tag,
            'attributes': element.attrib,
            'text': element.text.strip() if element.text else None,
            'children': []
        }
        
        for child in element:
            result['children'].append(self.to_dict(child))
        
        return result
    
    def to_string(self, encoding: str = 'unicode') -> str:
        """将XML转换为字符串"""
        return ET.tostring(self.root, encoding=encoding, method='xml')
    
    def save(self, file_path: str, encoding: str = 'utf-8'):
        """保存XML到文件"""
        self.tree.write(file_path, encoding=encoding, xml_declaration=True)
    
    def xpath(self, path: str) -> List[ET.Element]:
        """XPath查询（简化版）"""
        return self.root.findall(path) if self.root is not None else []
    
    def get_elements_by_tag(self, tag: str) -> List[ET.Element]:
        """根据标签名获取所有元素"""
        return self.root.findall(f".//{tag}") if self.root is not None else []
    
    def create_element(self, tag: str, text: Optional[str] = None, 
                      attrib: Optional[Dict[str, str]] = None) -> ET.Element:
        """创建新元素"""
        element = ET.Element(tag, attrib or {})
        if text:
            element.text = text
        return element
    
    def add_child(self, parent_path: str, child: ET.Element) -> bool:
        """向指定元素添加子元素"""
        parent = self.find(parent_path)
        if parent is not None:
            parent.append(child)
            return True
        return False
    
    def remove_element(self, path: str) -> bool:
        """删除元素"""
        parts = path.rsplit('/', 1)
        if len(parts) == 2:
            parent = self.find(parts[0])
            element = self.find(path)
            if parent is not None and element is not None:
                parent.remove(element)
                return True
        return False
    
    def pretty_print(self, indent: str = "  ") -> str:
        """格式化输出XML"""
        ET.indent(self.tree, space=indent)
        return self.to_string()


# 使用示例
if __name__ == "__main__":
    # 示例XML
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
    <bookstore>
        <book category="cooking">
            <title lang="en">Everyday Italian</title>
            <author>Giada De Laurentiis</author>
            <year>2005</year>
            <price>30.00</price>
        </book>
        <book category="children">
            <title lang="en">Harry Potter</title>
            <author>J K. Rowling</author>
            <year>2005</year>
            <price>29.99</price>
        </book>
    </bookstore>"""
    
    # 解析XML
    parser = XMLParser(xml_string=xml_data)
    
    # 查找元素
    print("第一本书标题:", parser.get_text("book/title"))
    
    # 获取属性
    print("第一本书分类:", parser.get_attribute("book", "category"))
    
    # 查找所有书籍
    books = parser.findall("book")
    print(f"共有 {len(books)} 本书")
    
    # 转换为字典
    print("\nXML字典格式:")
    print(parser.to_dict())