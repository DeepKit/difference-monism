import os
import time
from pathlib import Path
from typing import Callable, Dict, Set


class FileWatcher:
    def __init__(self, path: str, callback: Callable[[str, str], None]):
        """
        监控文件或目录变化
        
        Args:
            path: 要监控的文件或目录路径
            callback: 回调函数 callback(event_type, file_path)
                     event_type: 'created', 'modified', 'deleted'
        """
        self.path = Path(path)
        self.callback = callback
        self.running = False
        self._file_states: Dict[str, float] = {}
        
    def _scan(self) -> Set[str]:
        """扫描目录获取所有文件"""
        if self.path.is_file():
            return {str(self.path)}
        
        files = set()
        for item in self.path.rglob('*'):
            if item.is_file():
                files.add(str(item))
        return files
    
    def _get_mtime(self, filepath: str) -> float:
        """获取文件修改时间"""
        try:
            return os.path.getmtime(filepath)
        except OSError:
            return 0
    
    def start(self, interval: float = 1.0):
        """开始监控"""
        self.running = True
        
        # 初始化文件状态
        current_files = self._scan()
        for filepath in current_files:
            self._file_states[filepath] = self._get_mtime(filepath)
        
        while self.running:
            time.sleep(interval)
            
            current_files = self._scan()
            current_states = {f: self._get_mtime(f) for f in current_files}
            
            # 检测新建和修改
            for filepath, mtime in current_states.items():
                if filepath not in self._file_states:
                    self.callback('created', filepath)
                elif mtime != self._file_states[filepath]:
                    self.callback('modified', filepath)
            
            # 检测删除
            for filepath in self._file_states:
                if filepath not in current_states:
                    self.callback('deleted', filepath)
            
            self._file_states = current_states
    
    def stop(self):
        """停止监控"""
        self.running = False


# 使用示例
if __name__ == '__main__':
    def on_change(event_type, filepath):
        print(f'{event_type}: {filepath}')
    
    watcher = FileWatcher('.', on_change)
    try:
        watcher.start(interval=2.0)
    except KeyboardInterrupt:
        watcher.stop()