import importlib
import importlib.util
import inspect
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Type, Any


class Plugin(ABC):
    """插件基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本"""
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """初始化插件"""
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """执行插件主要功能"""
        pass
    
    def cleanup(self) -> None:
        """清理资源（可选）"""
        pass


class PluginLoader:
    """插件加载器"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_classes: Dict[str, Type[Plugin]] = {}
        
    def discover_plugins(self) -> List[str]:
        """发现插件目录中的所有插件"""
        if not self.plugin_dir.exists():
            self.plugin_dir.mkdir(parents=True, exist_ok=True)
            return []
        
        plugin_files = []
        for file_path in self.plugin_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                plugin_files.append(file_path.stem)
        
        return plugin_files
    
    def load_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """加载单个插件"""
        try:
            plugin_path = self.plugin_dir / f"{plugin_name}.py"
            
            if not plugin_path.exists():
                raise FileNotFoundError(f"插件文件不存在: {plugin_path}")
            
            # 动态导入模块
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"无法加载插件: {plugin_name}")
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)
            
            # 查找Plugin子类
            plugin_class = None
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Plugin) and obj is not Plugin:
                    plugin_class = obj
                    break
            
            if plugin_class is None:
                raise TypeError(f"插件 {plugin_name} 中未找到Plugin子类")
            
            # 实例化插件
            plugin_instance = plugin_class()
            plugin_instance.initialize()
            
            self.plugin_classes[plugin_name] = plugin_class
            self.plugins[plugin_instance.name] = plugin_instance
            
            return plugin_instance
            
        except Exception as e:
            print(f"加载插件 {plugin_name} 失败: {e}")
            return None
    
    def load_all_plugins(self) -> int:
        """加载所有插件"""
        plugin_names = self.discover_plugins()
        loaded_count = 0
        
        for plugin_name in plugin_names:
            if self.load_plugin(plugin_name):
                loaded_count += 1
        
        return loaded_count
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件"""
        if plugin_name in self.plugins:
            try:
                self.plugins[plugin_name].cleanup()
                del self.plugins[plugin_name]
                
                if plugin_name in self.plugin_classes:
                    del self.plugin_classes[plugin_name]
                
                if plugin_name in sys.modules:
                    del sys.modules[plugin_name]
                
                return True
            except Exception as e:
                print(f"卸载插件 {plugin_name} 失败: {e}")
                return False
        
        return False
    
    def reload_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """重新加载插件"""
        self.unload_plugin(plugin_name)
        return self.load_plugin(plugin_name)
    
    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """获取已加载的插件"""
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> List[str]:
        """列出所有已加载的插件"""
        return list(self.plugins.keys())
    
    def execute_plugin(self, plugin_name: str, *args, **kwargs) -> Any:
        """执行指定插件"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            return plugin.execute(*args, **kwargs)
        raise ValueError(f"插件 {plugin_name} 未加载")


# 使用示例
if __name__ == "__main__":
    # 创建插件加载器
    loader = PluginLoader("plugins")
    
    # 加载所有插件
    count = loader.load_all_plugins()
    print(f"已加载 {count} 个插件")
    
    # 列出插件
    print("已加载的插件:", loader.list_plugins())
    
    # 执行插件
    # result = loader.execute_plugin("my_plugin", arg1="value")