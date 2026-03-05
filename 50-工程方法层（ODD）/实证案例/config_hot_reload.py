import os
import json
import yaml
import configparser
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


class ConfigHotReload:
    """配置文件热加载类，支持JSON、YAML、INI格式"""
    
    def __init__(self, config_path: str, callback: Optional[Callable[[Dict], None]] = None):
        self.config_path = Path(config_path)
        self.callback = callback
        self.config: Dict[str, Any] = {}
        self.lock = threading.Lock()
        self.observer: Optional[Observer] = None
        self._last_modified = 0
        
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        self._load_config()
    
    def _load_config(self) -> None:
        """加载配置文件"""
        try:
            with self.lock:
                stat = self.config_path.stat()
                if stat.st_mtime == self._last_modified:
                    return
                
                self._last_modified = stat.st_mtime
                suffix = self.config_path.suffix.lower()
                
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    if suffix == '.json':
                        self.config = json.load(f)
                    elif suffix in ['.yaml', '.yml']:
                        self.config = yaml.safe_load(f)
                    elif suffix == '.ini':
                        parser = configparser.ConfigParser()
                        parser.read(self.config_path, encoding='utf-8')
                        self.config = {s: dict(parser.items(s)) for s in parser.sections()}
                    else:
                        raise ValueError(f"不支持的配置格式: {suffix}")
                
                print(f"配置已加载: {self.config_path}")
                
                if self.callback:
                    self.callback(self.config.copy())
                    
        except Exception as e:
            print(f"加载配置失败: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持点号分隔的嵌套键"""
        with self.lock:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                    if value is None:
                        return default
                else:
                    return default
            
            return value
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        with self.lock:
            return self.config.copy()
    
    def start_watch(self) -> None:
        """启动文件监控"""
        if self.observer:
            print("监控已启动")
            return
        
        event_handler = ConfigFileHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.config_path.parent), recursive=False)
        self.observer.start()
        print(f"开始监控配置文件: {self.config_path}")
    
    def stop_watch(self) -> None:
        """停止文件监控"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            print("停止监控配置文件")
    
    def reload(self) -> None:
        """手动重新加载配置"""
        self._load_config()
    
    def __enter__(self):
        self.start_watch()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_watch()


class ConfigFileHandler(FileSystemEventHandler):
    """文件系统事件处理器"""
    
    def __init__(self, config_loader: ConfigHotReload):
        self.config_loader = config_loader
        self._debounce_timer: Optional[threading.Timer] = None
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        if Path(event.src_path).resolve() == self.config_loader.config_path.resolve():
            # 防抖处理，避免重复加载
            if self._debounce_timer:
                self._debounce_timer.cancel()
            
            self._debounce_timer = threading.Timer(0.5, self._reload)
            self._debounce_timer.start()
    
    def _reload(self):
        try:
            self.config_loader.reload()
        except Exception as e:
            print(f"重新加载配置失败: {e}")


# 使用示例
if __name__ == "__main__":
    def on_config_change(config: Dict):
        print(f"配置已更新: {config}")
    
    # 创建示例配置文件
    example_config = {"database": {"host": "localhost", "port": 5432}, "debug": True}
    with open("config.json", "w") as f:
        json.dump(example_config, f)
    
    # 使用上下文管理器
    with ConfigHotReload("config.json", callback=on_config_change) as config:
        print(f"数据库主机: {config.get('database.host')}")
        print(f"调试模式: {config.get('debug')}")
        
        # 保持运行以测试热加载
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n退出程序")