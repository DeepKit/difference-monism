import pytest
from rbac_system import (
    RBACSystem, User, Role, RoleType, Permission,
    PermissionError, UserNotFoundError
)


@pytest.fixture
def rbac_system():
    return RBACSystem()


@pytest.fixture
def admin_user(rbac_system):
    return rbac_system.create_user("admin", RoleType.ADMIN)


@pytest.fixture
def normal_user(rbac_system):
    return rbac_system.create_user("user1", RoleType.USER)


@pytest.fixture
def guest_user(rbac_system):
    return rbac_system.create_user("guest1", RoleType.GUEST)


class TestUserCreation:
    def test_create_admin_user(self, rbac_system):
        user = rbac_system.create_user("admin", RoleType.ADMIN)
        assert user.username == "admin"
        assert user.role.name == RoleType.ADMIN
        assert user.user_id == 1
    
    def test_create_normal_user(self, rbac_system):
        user = rbac_system.create_user("user1", RoleType.USER)
        assert user.username == "user1"
        assert user.role.name == RoleType.USER
    
    def test_create_guest_user(self, rbac_system):
        user = rbac_system.create_user("guest1", RoleType.GUEST)
        assert user.username == "guest1"
        assert user.role.name == RoleType.GUEST
    
    def test_user_id_increment(self, rbac_system):
        user1 = rbac_system.create_user("user1", RoleType.USER)
        user2 = rbac_system.create_user("user2", RoleType.USER)
        assert user2.user_id == user1.user_id + 1


class TestPermissions:
    def test_admin_has_all_permissions(self, admin_user):
        assert admin_user.has_permission(Permission.READ_USER)
        assert admin_user.has_permission(Permission.WRITE_USER)
        assert admin_user.has_permission(Permission.DELETE_USER)
        assert admin_user.has_permission(Permission.READ_ROLE)
        assert admin_user.has_permission(Permission.WRITE_ROLE)
    
    def test_normal_user_permissions(self, normal_user):
        assert normal_user.has_permission(Permission.READ_OWN_DATA)
        assert normal_user.has_permission(Permission.WRITE_OWN_DATA)
        assert not normal_user.has_permission(Permission.READ_USER)
        assert not normal_user.has_permission(Permission.DELETE_USER)
    
    def test_guest_permissions(self, guest_user):
        assert guest_user.has_permission(Permission.READ_OWN_DATA)
        assert not guest_user.has_permission(Permission.WRITE_OWN_DATA)
        assert not guest_user.has_permission(Permission.READ_USER)


class TestListUsers:
    def test_admin_can_list_users(self, rbac_system, admin_user):
        rbac_system.create_user("user1", RoleType.USER)
        rbac_system.create_user("user2", RoleType.USER)
        users = rbac_system.list_users(admin_user)
        assert len(users) == 3
    
    def test_normal_user_cannot_list_users(self, rbac_system, normal_user):
        with pytest.raises(PermissionError) as exc_info:
            rbac_system.list_users(normal_user)
        assert "没有读取用户列表的权限" in str(exc_info.value)
    
    def test_guest_cannot_list_users(self, rbac_system, guest_user):
        with pytest.raises(PermissionError):
            rbac_system.list_users(guest_user)


class TestUpdateUser:
    def test_admin_can_update_any_user(self, rbac_system, admin_user, normal_user):
        data = {"email": "user@example.com", "age": 25}
        updated_user = rbac_system.update_user(admin_user, normal_user.user_id, data)
        assert updated_user.data["email"] == "user@example.com"
        assert updated_user.data["age"] == 25
    
    def test_user_can_update_own_data(self, rbac_system, normal_user):
        data = {"email": "myemail@example.com"}
        updated_user = rbac_system.update_user(normal_user, normal_user.user_id, data)
        assert updated_user.data["email"] == "myemail@example.com"
    
    def test_user_cannot_update_other_user_data(self, rbac_system, normal_user):
        other_user = rbac_system.create_user("user2", RoleType.USER)
        with pytest.raises(PermissionError) as exc_info:
            rbac_system.update_user(normal_user, other_user.user_id, {"email": "test@test.com"})
        assert "没有修改用户" in str(exc_info.value)
    
    def test_guest_cannot_update_own_data(self, rbac_system, guest_user):
        with pytest.raises(PermissionError):
            rbac_system.update_user(guest_user, guest_user.user_id, {"email": "guest@test.com"})


class TestDeleteUser:
    def test_admin_can_delete_user(self, rbac_system, admin_user):
        user_to_delete = rbac_system.create_user("temp_user", RoleType.USER)
        rbac_system.delete_user(admin_user, user_to_delete.user_id)
        with pytest.raises(UserNotFoundError):
            rbac_system.get_user(user_to_delete.user_id)
    
    def test_normal_user_cannot_delete_user(self, rbac_system, normal_user):
        user_to_delete = rbac_system.create_user("temp_user", RoleType.USER)
        with pytest.raises(PermissionError) as exc_info:
            rbac_system.delete_user(normal_user, user_to_delete.user_id)
        assert "没有删除用户的权限" in str(exc_info.value)
    
    def test_delete_nonexistent_user(self, rbac_system, admin_user):
        with pytest.raises(UserNotFoundError) as exc_info:
            rbac_system.delete_user(admin_user, 9999)
        assert "不存在" in str(exc_info.value)


class TestReadUserData:
    def test_admin_can_read_any_user_data(self, rbac_system, admin_user, normal_user):
        rbac_system.update_user(admin_user, normal_user.user_id, {"secret": "data"})
        data = rbac_system.read_user_data(admin_user, normal_user.user_id)
        assert data["secret"] == "data"
    
    def test_user_can_read_own_data(self, rbac_system, normal_user):
        rbac_system.update_user(normal_user, normal_user.user_id, {"my_data": "value"})
        data = rbac_system.read_user_data(normal_user, normal_user.user_id)
        assert data["my_data"] == "value"
    
    def test_user_cannot_read_other_user_data(self, rbac_system, normal_user):
        other_user = rbac_system.create_user("user2", RoleType.USER)
        with pytest.raises(PermissionError) as exc_info:
            rbac_system.read_user_data(normal_user, other_user.user_id)
        assert "没有读取用户" in str(exc_info.value)
    
    def test_guest_can_read_own_data(self, rbac_system, guest_user, admin_user):
        rbac_system.update_user(admin_user, guest_user.user_id, {"info": "test"})
        data = rbac_system.read_user_data(guest_user, guest_user.user_id)
        assert data["info"] == "test"


class TestChangeUserRole:
    def test_admin_can_change_user_role(self, rbac_system, admin_user, normal_user):
        updated_user = rbac_system.change_user_role(admin_user, normal_user.user_id, RoleType.ADMIN)
        assert updated_user.role.name == RoleType.ADMIN
        assert updated_user.has_permission(Permission.DELETE_USER)
    
    def test_normal_user_cannot_change_role(self, rbac_system, normal_user):
        other_user = rbac_system.create_user("user2", RoleType.USER)
        with pytest.raises(PermissionError) as exc_info:
            rbac_system.change_user_role(normal_user, other_user.user_id, RoleType.ADMIN)
        assert "没有修改角色的权限" in str(exc_info.value)
    
    def test_change_role_to_guest(self, rbac_system, admin_user, normal_user):
        updated_user = rbac_system.change_user_role(admin_user, normal_user.user_id, RoleType.GUEST)
        assert updated_user.role.name == RoleType.GUEST
        assert not updated_user.has_permission(Permission.WRITE_OWN_DATA)


class TestGetRolePermissions:
    def test_admin_can_get_role_permissions(self, rbac_system, admin_user):
        permissions = rbac_system.get_role_permissions(admin_user, RoleType.USER)
        assert Permission.READ_OWN_DATA in permissions
        assert Permission.WRITE_OWN_DATA in permissions
    
    def test_normal_user_cannot_get_role_permissions(self, rbac_system, normal_user):
        with pytest.raises(PermissionError) as exc_info:
            rbac_system.get_role_permissions(normal_user, RoleType.ADMIN)
        assert "没有读取角色权限的权限" in str(exc_info.value)


class TestComplexScenarios:
    def test_role_upgrade_scenario(self, rbac_system, admin_user):
        user = rbac_system.create_user("user1", RoleType.USER)
        user2 = rbac_system.create_user("user2", RoleType.USER)
        with pytest.raises(PermissionError):
            rbac_system.delete_user(user, user2.user_id)
        rbac_system.change_user_role(admin_user, user.user_id, RoleType.ADMIN)
        rbac_system.delete_user(user, user2.user_id)
        with pytest.raises(UserNotFoundError):
            rbac_system.get_user(user2.user_id)
    
    def test_data_isolation(self, rbac_system):
        user1 = rbac_system.create_user("user1", RoleType.USER)
        user2 = rbac_system.create_user("user2", RoleType.USER)
        rbac_system.update_user(user1, user1.user_id, {"private": "data1"})
        rbac_system.update_user(user2, user2.user_id, {"private": "data2"})
        data1 = rbac_system.read_user_data(user1, user1.user_id)
        data2 = rbac_system.read_user_data(user2, user2.user_id)
        assert data1["private"] == "data1"
        assert data2["private"] == "data2"
        with pytest.raises(PermissionError):
            rbac_system.read_user_data(user1, user2.user_id)
