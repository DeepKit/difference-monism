from abc import ABC, abstractmethod


class State(ABC):
    """状态抽象基类"""
    
    @abstractmethod
    def handle(self, context):
        pass


class DraftState(State):
    """草稿状态"""
    
    def handle(self, context):
        print("文档处于草稿状态，可以编辑")
        print("提交审核...")
        context.set_state(ReviewState())


class ReviewState(State):
    """审核状态"""
    
    def handle(self, context):
        print("文档正在审核中")
        print("审核通过，发布文档...")
        context.set_state(PublishedState())


class PublishedState(State):
    """已发布状态"""
    
    def handle(self, context):
        print("文档已发布，只读状态")
        print("撤回文档...")
        context.set_state(DraftState())


class Document:
    """上下文类"""
    
    def __init__(self):
        self._state = DraftState()
    
    def set_state(self, state: State):
        self._state = state
    
    def request(self):
        self._state.handle(self)


# 使用示例
if __name__ == "__main__":
    doc = Document()
    
    doc.request()  # 草稿 -> 审核
    print()
    
    doc.request()  # 审核 -> 发布
    print()
    
    doc.request()  # 发布 -> 草稿