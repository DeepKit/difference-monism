from datetime import datetime
from typing import List, Dict, Any, Type
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import uuid


@dataclass
class Event:
    """基础事件类"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    aggregate_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    version: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "version": self.version
        }


class EventStore:
    """事件存储"""
    def __init__(self):
        self._events: Dict[str, List[Event]] = {}

    def save(self, event: Event) -> None:
        if event.aggregate_id not in self._events:
            self._events[event.aggregate_id] = []
        self._events[event.aggregate_id].append(event)

    def get_events(self, aggregate_id: str, from_version: int = 0) -> List[Event]:
        events = self._events.get(aggregate_id, [])
        return [e for e in events if e.version >= from_version]

    def get_all_events(self) -> List[Event]:
        all_events = []
        for events in self._events.values():
            all_events.extend(events)
        return sorted(all_events, key=lambda e: e.timestamp)


class AggregateRoot(ABC):
    """聚合根基类"""
    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self.version = 0
        self._uncommitted_events: List[Event] = []

    def apply_event(self, event: Event) -> None:
        """应用事件到聚合"""
        event.aggregate_id = self.aggregate_id
        event.version = self.version + 1
        self._apply(event)
        self.version = event.version
        self._uncommitted_events.append(event)

    @abstractmethod
    def _apply(self, event: Event) -> None:
        """子类实现具体的事件应用逻辑"""
        pass

    def load_from_history(self, events: List[Event]) -> None:
        """从历史事件重建状态"""
        for event in events:
            self._apply(event)
            self.version = event.version

    def get_uncommitted_events(self) -> List[Event]:
        return self._uncommitted_events.copy()

    def mark_events_as_committed(self) -> None:
        self._uncommitted_events.clear()


# 示例：银行账户聚合
class AccountCreated(Event):
    def __init__(self, account_id: str, owner: str, initial_balance: float = 0):
        super().__init__(
            event_type="AccountCreated",
            aggregate_id=account_id,
            data={"owner": owner, "initial_balance": initial_balance}
        )


class MoneyDeposited(Event):
    def __init__(self, account_id: str, amount: float):
        super().__init__(
            event_type="MoneyDeposited",
            aggregate_id=account_id,
            data={"amount": amount}
        )


class MoneyWithdrawn(Event):
    def __init__(self, account_id: str, amount: float):
        super().__init__(
            event_type="MoneyWithdrawn",
            aggregate_id=account_id,
            data={"amount": amount}
        )


class BankAccount(AggregateRoot):
    """银行账户聚合"""
    def __init__(self, account_id: str):
        super().__init__(account_id)
        self.owner = ""
        self.balance = 0.0

    def create_account(self, owner: str, initial_balance: float = 0) -> None:
        if self.owner:
            raise ValueError("账户已存在")
        event = AccountCreated(self.aggregate_id, owner, initial_balance)
        self.apply_event(event)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("存款金额必须大于0")
        event = MoneyDeposited(self.aggregate_id, amount)
        self.apply_event(event)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("取款金额必须大于0")
        if self.balance < amount:
            raise ValueError("余额不足")
        event = MoneyWithdrawn(self.aggregate_id, amount)
        self.apply_event(event)

    def _apply(self, event: Event) -> None:
        if event.event_type == "AccountCreated":
            self.owner = event.data["owner"]
            self.balance = event.data["initial_balance"]
        elif event.event_type == "MoneyDeposited":
            self.balance += event.data["amount"]
        elif event.event_type == "MoneyWithdrawn":
            self.balance -= event.data["amount"]


class Repository:
    """仓储层"""
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def save(self, aggregate: AggregateRoot) -> None:
        for event in aggregate.get_uncommitted_events():
            self.event_store.save(event)
        aggregate.mark_events_as_committed()

    def get_by_id(self, aggregate_id: str, aggregate_class: Type[AggregateRoot]) -> AggregateRoot:
        events = self.event_store.get_events(aggregate_id)
        aggregate = aggregate_class(aggregate_id)
        aggregate.load_from_history(events)
        return aggregate


# 使用示例
if __name__ == "__main__":
    # 初始化
    event_store = EventStore()
    repository = Repository(event_store)

    # 创建账户
    account = BankAccount("acc-001")
    account.create_account("张三", 1000.0)
    repository.save(account)

    # 存款
    account.deposit(500.0)
    repository.save(account)

    # 取款
    account.withdraw(200.0)
    repository.save(account)

    print(f"当前余额: {account.balance}")
    print(f"版本: {account.version}")

    # 从事件重建状态
    rebuilt_account = repository.get_by_id("acc-001", BankAccount)
    print(f"\n重建后的余额: {rebuilt_account.balance}")
    print(f"账户所有者: {rebuilt_account.owner}")

    # 查看所有事件
    print("\n事件历史:")
    for event in event_store.get_events("acc-001"):
        print(f"  {event.event_type} - 版本{event.version}: {event.data}")