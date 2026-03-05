# 方法1: 使用元类（推荐）
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def __init__(self):
        self.value = None


# 方法2: 使用装饰器
def singleton(cls):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Singleton2:
    def __init__(self):
        self.value = None


# 方法3: 使用__new__方法
class Singleton3:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.value = None


# 使用示例
if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()
    print(s1 is s2)  # True
    
    s3 = Singleton2()
    s4 = Singleton2()
    print(s3 is s4)  # True
    
    s5 = Singleton3()
    s6 = Singleton3()
    print(s5 is s6)  # True