from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """观察者抽象类"""
    
    @abstractmethod
    def update(self, subject: 'Subject') -> None:
        pass


class Subject:
    """被观察者/主题类"""
    
    def __init__(self):
        self._observers: List[Observer] = []
        self._state = None
    
    def attach(self, observer: Observer) -> None:
        """添加观察者"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """移除观察者"""
        self._observers.remove(observer)
    
    def notify(self) -> None:
        """通知所有观察者"""
        for observer in self._observers:
            observer.update(self)
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
        self.notify()


class ConcreteObserverA(Observer):
    """具体观察者A"""
    
    def update(self, subject: Subject) -> None:
        print(f"ObserverA: 收到状态更新 -> {subject.state}")


class ConcreteObserverB(Observer):
    """具体观察者B"""
    
    def update(self, subject: Subject) -> None:
        print(f"ObserverB: 状态变化为 -> {subject.state}")


# 使用示例
if __name__ == "__main__":
    subject = Subject()
    
    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()
    
    subject.attach(observer_a)
    subject.attach(observer_b)
    
    subject.state = "状态1"
    subject.state = "状态2"
    
    subject.detach(observer_a)
    subject.state = "状态3"