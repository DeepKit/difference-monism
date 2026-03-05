from enum import Enum
from typing import Set, Dict, Optional, List
from dataclasses import dataclass, field


class Permission(Enum):
    READ_USER = "read_user"
    WRITE_USER = "write_user"
    DELETE_USER = "delete_user"
    READ_ROLE = "read_role"
    WRITE_ROLE = "write_role"
    READ_OWN_DATA = "read_own_data"
    WRITE_OWN_DATA = "write_own_data"


class RoleType(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


@dataclass
class Role:
    name: RoleType
    permissions: Set[Permission] = field(default_factory=set)
    
    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions


@dataclass
class User:
    user_id: int
    username: str
    role: Role
    data: Dict = field(default_factory=dict)
    
    def has_permission(self, permission: Permission) -> bool:
        return self.role.has_permission(permission)


class PermissionError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class RBACSystem:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.roles: Dict[RoleType, Role] = self._init_roles()
        self._user_id_counter = 1
    
    def _init_roles(self) -> Dict[RoleType, Role]:
        return {
            RoleType.ADMIN: Role(
                name=RoleType.ADMIN,
                permissions={
                    Permission.READ_USER,
                    Permission.WRITE_USER,
                    Permission.DELETE_USER,
                    Permission.READ_ROLE,
                    Permission.WRITE_ROLE,
                    Permission.READ_OWN_DATA,
                    Permission.WRITE_OWN_DATA,
                }
            ),
            RoleType.USER: Role(
                name=RoleType.USER,
                permissions={
                    Permission.READ_OWN_DATA,
                    Permission.WRITE_OWN_DATA,
                }
            ),
            RoleType.GUEST: Role(
                name=RoleType.GUEST,
                permissions={
                    Permission.READ_OWN_DATA,
                }
            ),
        }
    
    def create_user(self, username: str, role_type: RoleType) -> User:
        role = self.roles[role_type]
        user = User(user_id=self._user_id_counter, username=username, role=role)
        self.users[user.user_id] = user
        self._user_id_counter += 1
        return user
    
    def get_user(self, user_id: int) -> User:
        if user_id not in self.users:
            raise UserNotFoundError(f"用户ID {user_id} 不存在")
        return self.users[user_id]
    
    def list_users(self, current_user: User) -> List[User]:
        if not current_user.has_permission(Permission.READ_USER):
            raise PermissionError(f"用户 {current_user.username} 没有读取用户列表的权限")
        return list(self.users.values())
    
    def update_user(self, current_user: User, target_user_id: int, data: Dict) -> User:
        target_user = self.get_user(target_user_id)
        
        if current_user.has_permission(Permission.WRITE_USER):
            target_user.data.update(data)
            return target_user
        
        if current_user.user_id == target_user_id and \
           current_user.has_permission(Permission.WRITE_OWN_DATA):
            target_user.data.update(data)
            return target_user
        
        raise PermissionError(f"用户 {current_user.username} 没有修改用户 {target_user.username} 数据的权限")
    
    def delete_user(self, current_user: User, target_user_id: int) -> None:
        if not current_user.has_permission(Permission.DELETE_USER):
            raise PermissionError(f"用户 {current_user.username} 没有删除用户的权限")
        
        if target_user_id not in self.users:
            raise UserNotFoundError(f"用户ID {target_user_id} 不存在")
        
        del self.users[target_user_id]
    
    def read_user_data(self, current_user: User, target_user_id: int) -> Dict:
        target_user = self.get_user(target_user_id)
        
        if current_user.has_permission(Permission.READ_USER):
            return target_user.data
        
        if current_user.user_id == target_user_id and \
           current_user.has_permission(Permission.READ_OWN_DATA):
            return target_user.data
        
        raise PermissionError(f"用户 {current_user.username} 没有读取用户 {target_user.username} 数据的权限")
    
    def change_user_role(self, current_user: User, target_user_id: int, 
                        new_role_type: RoleType) -> User:
        if not current_user.has_permission(Permission.WRITE_ROLE):
            raise PermissionError(f"用户 {current_user.username} 没有修改角色的权限")
        
        target_user = self.get_user(target_user_id)
        target_user.role = self.roles[new_role_type]
        return target_user
    
    def get_role_permissions(self, current_user: User, role_type: RoleType) -> Set[Permission]:
        if not current_user.has_permission(Permission.READ_ROLE):
            raise PermissionError(f"用户 {current_user.username} 没有读取角色权限的权限")
        return self.roles[role_type].permissions