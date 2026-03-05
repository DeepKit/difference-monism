from typing import List
from datetime import datetime


class Memento:
    """备忘录类 - 存储发起人的状态"""
    
    def __init__(self, state: str):
        self._state = state
        self._timestamp = datetime.now()
    
    def get_state(self) -> str:
        return self._state
    
    def get_timestamp(self) -> datetime:
        return self._timestamp


class TextEditor:
    """发起人类 - 文本编辑器"""
    
    def __init__(self):
        self._content = ""
    
    def write(self, text: str):
        """写入文本"""
        self._content += text
        print(f"当前内容: {self._content}")
    
    def get_content(self) -> str:
        return self._content
    
    def save(self) -> Memento:
        """保存当前状态到备忘录"""
        print(f"保存状态: {self._content}")
        return Memento(self._content)
    
    def restore(self, memento: Memento):
        """从备忘录恢复状态"""
        self._content = memento.get_state()
        print(f"恢复到: {self._content}")


class History:
    """管理者类 - 管理备忘录历史"""
    
    def __init__(self):
        self._mementos: List[Memento] = []
    
    def push(self, memento: Memento):
        """保存备忘录"""
        self._mementos.append(memento)
    
    def pop(self) -> Memento:
        """获取最近的备忘录"""
        if not self._mementos:
            return None
        return self._mementos.pop()
    
    def show_history(self):
        """显示历史记录"""
        print("\n历史记录:")
        for i, memento in enumerate(self._mementos):
            print(f"{i + 1}. {memento.get_state()} - {memento.get_timestamp()}")


if __name__ == "__main__":
    editor = TextEditor()
    history = History()
    
    # 编辑文本并保存状态
    editor.write("Hello ")
    history.push(editor.save())
    
    editor.write("World")
    history.push(editor.save())
    
    editor.write("!")
    history.push(editor.save())
    
    # 显示历史
    history.show_history()
    
    # 撤销操作
    print("\n执行撤销:")
    editor.restore(history.pop())
    editor.restore(history.pop())
    
    # 继续编辑
    print("\n继续编辑:")
    editor.write(" Python")
    history.push(editor.save())