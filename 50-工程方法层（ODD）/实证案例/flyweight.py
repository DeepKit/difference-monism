from typing import Dict
import weakref


class Flyweight:
    """享元基类"""
    def __init__(self, intrinsic_state: str):
        self.intrinsic_state = intrinsic_state
    
    def operation(self, extrinsic_state: str) -> str:
        return f"内部状态: {self.intrinsic_state}, 外部状态: {extrinsic_state}"


class ConcreteFlyweight(Flyweight):
    """具体享元类"""
    def operation(self, extrinsic_state: str) -> str:
        return f"[具体享元] {super().operation(extrinsic_state)}"


class FlyweightFactory:
    """享元工厂"""
    def __init__(self):
        self._flyweights: Dict[str, Flyweight] = {}
    
    def get_flyweight(self, key: str) -> Flyweight:
        """获取享元对象，如果不存在则创建"""
        if key not in self._flyweights:
            print(f"创建新的享元对象: {key}")
            self._flyweights[key] = ConcreteFlyweight(key)
        else:
            print(f"复用已有享元对象: {key}")
        return self._flyweights[key]
    
    def get_flyweight_count(self) -> int:
        """获取享元对象数量"""
        return len(self._flyweights)
    
    def list_flyweights(self):
        """列出所有享元对象"""
        print(f"\n享元工厂中共有 {self.get_flyweight_count()} 个享元对象:")
        for key in self._flyweights.keys():
            print(f"  - {key}")


# 实际应用示例：文本编辑器中的字符
class Character(Flyweight):
    """字符享元类"""
    def __init__(self, char: str):
        super().__init__(char)
        self.char = char
    
    def render(self, font: str, size: int, color: str, position: tuple) -> str:
        """渲染字符（外部状态：字体、大小、颜色、位置）"""
        return (f"字符 '{self.char}' - "
                f"字体:{font}, 大小:{size}, 颜色:{color}, 位置:{position}")


class CharacterFactory:
    """字符工厂"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._characters = {}
        return cls._instance
    
    def get_character(self, char: str) -> Character:
        """获取字符对象"""
        if char not in self._characters:
            self._characters[char] = Character(char)
        return self._characters[char]
    
    def get_character_count(self) -> int:
        return len(self._characters)


if __name__ == "__main__":
    print("=== 基础享元模式示例 ===\n")
    
    factory = FlyweightFactory()
    
    # 创建和使用享元对象
    flyweight1 = factory.get_flyweight("状态A")
    print(flyweight1.operation("外部数据1"))
    
    flyweight2 = factory.get_flyweight("状态B")
    print(flyweight2.operation("外部数据2"))
    
    flyweight3 = factory.get_flyweight("状态A")  # 复用
    print(flyweight3.operation("外部数据3"))
    
    # 验证对象是否相同
    print(f"\nflyweight1 和 flyweight3 是同一个对象: {flyweight1 is flyweight3}")
    
    factory.list_flyweights()
    
    print("\n\n=== 文本编辑器字符示例 ===\n")
    
    char_factory = CharacterFactory()
    text = "HELLO WORLD"
    
    # 模拟渲染文本
    for i, char in enumerate(text):
        if char != ' ':
            character = char_factory.get_character(char)
            print(character.render("Arial", 12, "black", (i * 10, 0)))
    
    print(f"\n文本 '{text}' 包含 {len(text)} 个字符")
    print(f"但只创建了 {char_factory.get_character_count()} 个字符对象")
    print(f"节省内存: {len(text) - char_factory.get_character_count()} 个对象")