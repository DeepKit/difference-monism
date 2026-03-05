# domain/events.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class DomainEvent:
    event_id: str = None
    occurred_at: datetime = None
    
    def __post_init__(self):
        if not self.event_id:
            self.event_id = str(uuid4())
        if not self.occurred_at:
            self.occurred_at = datetime.utcnow()


# cqrs/commands.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Type


@dataclass
class Command(ABC):
    pass


class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command) -> Any:
        pass


class CommandBus:
    def __init__(self):
        self._handlers: Dict[Type[Command], CommandHandler] = {}
    
    def register(self, command_type: Type[Command], handler: CommandHandler):
        self._handlers[command_type] = handler
    
    def execute(self, command: Command) -> Any:
        handler = self._handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler registered for {type(command).__name__}")
        return handler.handle(command)


# cqrs/queries.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Type


@dataclass
class Query(ABC):
    pass


class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query) -> Any:
        pass


class QueryBus:
    def __init__(self):
        self._handlers: Dict[Type[Query], QueryHandler] = {}
    
    def register(self, query_type: Type[Query], handler: QueryHandler):
        self._handlers[query_type] = handler
    
    def execute(self, query: Query) -> Any:
        handler = self._handlers.get(type(query))
        if not handler:
            raise ValueError(f"No handler registered for {type(query).__name__}")
        return handler.handle(query)


# example/models.py
from dataclasses import dataclass, field
from typing import List
from domain.events import DomainEvent


@dataclass
class UserCreated(DomainEvent):
    user_id: str = None
    email: str = None
    name: str = None


@dataclass
class User:
    id: str
    email: str
    name: str
    events: List[DomainEvent] = field(default_factory=list)
    
    def add_event(self, event: DomainEvent):
        self.events.append(event)


# example/commands.py
from dataclasses import dataclass
from cqrs.commands import Command, CommandHandler
from example.models import User, UserCreated
from uuid import uuid4


@dataclass
class CreateUserCommand(Command):
    email: str
    name: str


@dataclass
class UpdateUserCommand(Command):
    user_id: str
    name: str


class CreateUserHandler(CommandHandler):
    def __init__(self, repository):
        self.repository = repository
    
    def handle(self, command: CreateUserCommand) -> str:
        user_id = str(uuid4())
        user = User(id=user_id, email=command.email, name=command.name)
        
        event = UserCreated(user_id=user_id, email=command.email, name=command.name)
        user.add_event(event)
        
        self.repository.save(user)
        return user_id


class UpdateUserHandler(CommandHandler):
    def __init__(self, repository):
        self.repository = repository
    
    def handle(self, command: UpdateUserCommand) -> None:
        user = self.repository.get_by_id(command.user_id)
        if not user:
            raise ValueError(f"User {command.user_id} not found")
        
        user.name = command.name
        self.repository.save(user)


# example/queries.py
from dataclasses import dataclass
from typing import List, Optional
from cqrs.queries import Query, QueryHandler
from example.models import User


@dataclass
class GetUserByIdQuery(Query):
    user_id: str


@dataclass
class GetAllUsersQuery(Query):
    pass


@dataclass
class UserDTO:
    id: str
    email: str
    name: str


class GetUserByIdHandler(QueryHandler):
    def __init__(self, read_repository):
        self.read_repository = read_repository
    
    def handle(self, query: GetUserByIdQuery) -> Optional[UserDTO]:
        user = self.read_repository.get_by_id(query.user_id)
        if not user:
            return None
        return UserDTO(id=user.id, email=user.email, name=user.name)


class GetAllUsersHandler(QueryHandler):
    def __init__(self, read_repository):
        self.read_repository = read_repository
    
    def handle(self, query: GetAllUsersQuery) -> List[UserDTO]:
        users = self.read_repository.get_all()
        return [UserDTO(id=u.id, email=u.email, name=u.name) for u in users]


# infrastructure/repositories.py
from typing import Dict, List, Optional
from example.models import User


class InMemoryUserRepository:
    def __init__(self):
        self._users: Dict[str, User] = {}
    
    def save(self, user: User):
        self._users[user.id] = user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def get_all(self) -> List[User]:
        return list(self._users.values())


# main.py
from cqrs.commands import CommandBus
from cqrs.queries import QueryBus
from example.commands import CreateUserCommand, CreateUserHandler, UpdateUserCommand, UpdateUserHandler
from example.queries import GetUserByIdQuery, GetUserByIdHandler, GetAllUsersQuery, GetAllUsersHandler
from infrastructure.repositories import InMemoryUserRepository


def main():
    # Setup
    repository = InMemoryUserRepository()
    
    command_bus = CommandBus()
    command_bus.register(CreateUserCommand, CreateUserHandler(repository))
    command_bus.register(UpdateUserCommand, UpdateUserHandler(repository))
    
    query_bus = QueryBus()
    query_bus.register(GetUserByIdQuery, GetUserByIdHandler(repository))
    query_bus.register(GetAllUsersQuery, GetAllUsersHandler(repository))
    
    # Create user
    user_id = command_bus.execute(CreateUserCommand(
        email="user@example.com",
        name="John Doe"
    ))
    print(f"Created user: {user_id}")
    
    # Query user
    user = query_bus.execute(GetUserByIdQuery(user_id=user_id))
    print(f"User: {user}")
    
    # Update user
    command_bus.execute(UpdateUserCommand(user_id=user_id, name="Jane Doe"))
    
    # Query updated user
    user = query_bus.execute(GetUserByIdQuery(user_id=user_id))
    print(f"Updated user: {user}")
    
    # Query all users
    users = query_bus.execute(GetAllUsersQuery())
    print(f"All users: {users}")


if __name__ == "__main__":
    main()