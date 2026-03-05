from abc import ABC, abstractmethod
from typing import List


# 命令接口
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass


# 接收者：文本编辑器
class TextEditor:
    def __init__(self):
        self.text = ""
    
    def write(self, text: str):
        self.text += text
        print(f"写入: '{text}' | 当前内容: '{self.text}'")
    
    def delete(self, length: int):
        deleted = self.text[-length:] if length <= len(self.text) else self.text
        self.text = self.text[:-length] if length <= len(self.text) else ""
        print(f"删除: '{deleted}' | 当前内容: '{self.text}'")
        return deleted
    
    def get_text(self):
        return self.text


# 具体命令：写入命令
class WriteCommand(Command):
    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text
    
    def execute(self):
        self.editor.write(self.text)
    
    def undo(self):
        self.editor.delete(len(self.text))


# 具体命令：删除命令
class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, length: int):
        self.editor = editor
        self.length = length
        self.deleted_text = ""
    
    def execute(self):
        self.deleted_text = self.editor.delete(self.length)
    
    def undo(self):
        self.editor.write(self.deleted_text)


# 调用者：命令管理器
class CommandManager:
    def __init__(self):
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []
    
    def execute_command(self, command: Command):
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()
    
    def undo(self):
        if not self.history:
            print("没有可撤销的操作")
            return
        
        command = self.history.pop()
        command.undo()
        self.redo_stack.append(command)
    
    def redo(self):
        if not self.redo_stack:
            print("没有可重做的操作")
            return
        
        command = self.redo_stack.pop()
        command.execute()
        self.history.append(command)


# 客户端代码
if __name__ == "__main__":
    editor = TextEditor()
    manager = CommandManager()
    
    # 执行命令
    manager.execute_command(WriteCommand(editor, "Hello "))
    manager.execute_command(WriteCommand(editor, "World!"))
    manager.execute_command(DeleteCommand(editor, 6))
    manager.execute_command(WriteCommand(editor, "Python!"))
    
    print("\n--- 撤销操作 ---")
    manager.undo()
    manager.undo()
    
    print("\n--- 重做操作 ---")
    manager.redo()
    
    print(f"\n最终文本: '{editor.get_text()}'")