
import pytest
from threading import Thread
from time import sleep


class OptimisticLock:
    """示例实现 - 实际测试时替换为你的实现"""
    def __init__(self, initial_value=None):
        self.value = initial_value
        self.version = 0
    
    def read(self):
        return self.value, self.version
    
    def write(self, new_value, expected_version):
        if self.version != expected_version:
            return False
        self.value = new_value
        self.version += 1
        return True


# 基本功能测试
def test_initial_state():
    lock = OptimisticLock("initial")
    value, version = lock.read()
    assert value == "initial"
    assert version == 0


def test_successful_write():
    lock = OptimisticLock("data")
    value, version = lock.read()
    assert lock.write("new_data", version) is True
    new_value, new_version = lock.read()
    assert new_value == "new_data"
    assert new_version == 1


def test_write_with_stale_version():
    lock = OptimisticLock("data")
    _, version = lock.read()
    lock.write("update1", version)
    # 使用旧版本号写入应该失败
    assert lock.write("update2", version) is False


def test_concurrent_modification():
    lock = OptimisticLock(0)
    
    def increment():
        value, version = lock.read()
        sleep(0.01)  # 模拟处理时间
        return lock.write(value + 1, version)
    
    threads = [Thread(target=increment) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # 只有一个线程应该成功
    final_value, _ = lock.read()
    assert final_value == 1


def test_multiple_sequential_writes():
    lock = OptimisticLock(0)
    for i in range(5):
        value, version = lock.read()
        assert lock.write(value + 1, version) is True
    
    final_value, final_version = lock.read()
    assert final_value == 5
    assert final_version == 5


@pytest.mark.parametrize("initial,updates", [
    (0, [1, 2, 3]),
    ("a", ["b", "c", "d"]),
    ([], [[1], [1, 2], [1, 2, 3]]),
])
def test_various_data_types(initial, updates):
    lock = OptimisticLock(initial)
    for update in updates:
        value, version = lock.read()
        assert lock.write(update, version) is True
    
    final_value, _ = lock.read()
    assert final_value == updates[-1]
