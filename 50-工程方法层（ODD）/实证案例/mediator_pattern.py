from abc import ABC, abstractmethod
from typing import List


class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: object, event: str) -> None:
        pass


class Colleague(ABC):
    def __init__(self, mediator: Mediator = None):
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator


class ChatRoom(Mediator):
    def __init__(self):
        self._users: List['User'] = []

    def register_user(self, user: 'User') -> None:
        self._users.append(user)
        user.mediator = self

    def notify(self, sender: 'User', event: str) -> None:
        if event == "send_message":
            for user in self._users:
                if user != sender:
                    user.receive(sender.last_message, sender.name)


class User(Colleague):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.last_message = ""

    def send(self, message: str) -> None:
        print(f"{self.name} 发送: {message}")
        self.last_message = message
        self.mediator.notify(self, "send_message")

    def receive(self, message: str, sender_name: str) -> None:
        print(f"{self.name} 收到来自 {sender_name} 的消息: {message}")


# 使用示例
if __name__ == "__main__":
    chat_room = ChatRoom()

    alice = User("Alice")
    bob = User("Bob")
    charlie = User("Charlie")

    chat_room.register_user(alice)
    chat_room.register_user(bob)
    chat_room.register_user(charlie)

    alice.send("大家好！")
    print()
    bob.send("你好 Alice！")
    print()
    charlie.send("嗨，大家！")