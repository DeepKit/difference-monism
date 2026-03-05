from enum import Enum
from typing import Set, Optional, Any
from dataclasses import dataclass


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    READ_ALL = "read_all"
    WRITE_ALL = "write_all"
    DELETE_ALL = "delete_all"


class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


@dataclass
class User:
    id: int
    name: str
    role: Role
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class Resource:
    id: int
    owner_id: int
    content: Any


class RBACSystem:
    def __init__(self):
        self.role_permissions = {
            Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.READ_ALL, Permission.WRITE_ALL, Permission.DELETE_ALL},
            Role.USER: {Permission.READ, Permission.WRITE},
            Role.GUEST: {Permission.READ}
        }
    
    def get_permissions(self, role: Role) -> Set[Permission]:
        return self.role_permissions.get(role, set())
    
    def check_permission(self, user: User, permission: Permission, resource: Optional[Resource] = None) -> tuple[bool, str]:
        user_permissions = self.get_permissions(user.role)
        
        if user.role == Role.ADMIN:
            return True, ""
        
        if permission == Permission.READ and Permission.READ_ALL in user_permissions:
            return True, ""
        if permission == Permission.WRITE and Permission.WRITE_ALL in user_permissions:
            return True, ""
        if permission == Permission.DELETE and Permission.DELETE_ALL in user_permissions:
            return True, ""
        
        if permission not in user_permissions:
            return False, f"用户角色 '{user.role.value}' 没有 '{permission.value}' 权限"
        
        if resource is not None:
            if resource.owner_id != user.id:
                return False, f"用户 '{user.name}' 无权访问其他用户的数据"
        
        return True, ""
    
    def can_read(self, user: User, resource: Resource) -> tuple[bool, str]:
        return self.check_permission(user, Permission.READ, resource)
    
    def can_write(self, user: User, resource: Resource) -> tuple[bool, str]:
        return self.check_permission(user, Permission.WRITE, resource)
    
    def can_delete(self, user: User, resource: Resource) -> tuple[bool, str]:
        return self.check_permission(user, Permission.DELETE, resource)
    
    def read_resource(self, user: User, resource: Resource) -> tuple[bool, Any, str]:
        allowed, error = self.can_read(user, resource)
        if not allowed:
            return False, None, error
        return True, resource.content, ""
    
    def write_resource(self, user: User, resource: Resource, new_content: Any) -> tuple[bool, str]:
        allowed, error = self.can_write(user, resource)
        if not allowed:
            return False, error
        resource.content = new_content
        return True, ""
    
    def delete_resource(self, user: User, resource: Resource) -> tuple[bool, str]:
        allowed, error = self.can_delete(user, resource)
        if not allowed:
            return False, error
        return True, ""
