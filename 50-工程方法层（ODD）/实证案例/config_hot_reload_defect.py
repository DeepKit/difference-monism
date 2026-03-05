import json
import os
import threading
import time
from typing import Any, Callable, Optional


class ConfigHotReload:
    def __init__(
        self,
        config_path: str,
        check_interval: float = 1.0,
        on_reload: Optional[Callable[[dict], None]] = None
    ):
        """
        配置热加载类
        
        Args:
            config_path: 配置文件路径
            check_interval: 检查间隔（秒）
            on_reload: 配置重载时的回调函数
        """
        self.config_path = config_path
        self.check_interval = check_interval
        self.on_reload = on_reload
        
        self._config: dict = {}
        self._last_mtime: float = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        
        # 初始加载
        self._load_config()
    
    def _load_config(self) -> None:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            self._last_mtime = os.path.getmtime(self.config_path)
            
            if self.on_reload:
                self.on_reload(self._config)
        except Exception as e:
            print(f"加载配置失败: {e}")
    
    def _check_and_reload(self) -> None:
        """检查文件变化并重载"""
        try:
            current_mtime = os.path.getmtime(self.config_path)
            if current_mtime > self._last_mtime:
                print(f"检测到配置变化，重新加载: {self.config_path}")
                self._load_config()
        except Exception as e:
            print(f"检查配置失败: {e}")
    
    def _watch_loop(self) -> None:
        """监控循环"""
        while self._running:
            self._check_and_reload()
            time.sleep(self.check_interval)
    
    def start(self) -> None:
        """启动热加载监控"""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._watch_loop, daemon=True)
            self._thread.start()
            print(f"配置热加载已启动: {self.config_path}")
    
    def stop(self) -> None:
        """停止热加载监控"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        print("配置热加载已停止")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value
    
    @property
    def config(self) -> dict:
        """获取完整配置"""
        return self._config.copy()


# 使用示例
if __name__ == "__main__":
    def on_config_change(config):
        print(f"配置已更新: {config}")
    
    # 创建示例配置文件
    example_config = {
        "database": {
            "host": "localhost",
            "port": 5432
        },
        "debug": True
    }
    
    with open("config.json", "w") as f:
        json.dump(example_config, f, indent=2)
    
    # 初始化热加载
    config = ConfigHotReload("config.json", check_interval=2.0, on_reload=on_config_change)
    config.start()
    
    # 使用配置
    print(f"数据库主机: {config.get('database.host')}")
    print(f"调试模式: {config.get('debug')}")
    
    # 保持运行以测试热加载
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        config.stop()