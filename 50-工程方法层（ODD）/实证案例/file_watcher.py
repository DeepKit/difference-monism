import os
import time
import threading
from pathlib import Path
from typing import Callable, Optional, List, Set
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventType(Enum):
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"


@dataclass
class FileEvent:
    event_type: EventType
    path: str
    is_directory: bool
    timestamp: float
    src_path: Optional[str] = None


class FileWatcher:
    def __init__(
        self,
        path: str,
        recursive: bool = True,
        patterns: Optional[List[str]] = None,
        ignore_patterns: Optional[List[str]] = None,
    ):
        self.path = Path(path).resolve()
        self.recursive = recursive
        self.patterns = patterns or ["*"]
        self.ignore_patterns = ignore_patterns or []
        self._callbacks: List[Callable[[FileEvent], None]] = []
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._file_states: dict = {}
        self._lock = threading.Lock()
        
        if not self.path.exists():
            raise FileNotFoundError(f"Path does not exist: {self.path}")

    def add_callback(self, callback: Callable[[FileEvent], None]) -> None:
        with self._lock:
            self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[FileEvent], None]) -> None:
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

    def _should_watch(self, path: Path) -> bool:
        path_str = str(path)
        
        for ignore_pattern in self.ignore_patterns:
            if self._match_pattern(path_str, ignore_pattern):
                return False
        
        for pattern in self.patterns:
            if self._match_pattern(path_str, pattern):
                return True
        
        return False

    def _match_pattern(self, path: str, pattern: str) -> bool:
        if pattern == "*":
            return True
        if pattern.startswith("*."):
            return path.endswith(pattern[1:])
        if "*" in pattern:
            import fnmatch
            return fnmatch.fnmatch(path, pattern)
        return pattern in path

    def _scan_directory(self) -> dict:
        states = {}
        try:
            if self.recursive:
                for root, dirs, files in os.walk(self.path):
                    root_path = Path(root)
                    for name in files:
                        file_path = root_path / name
                        if self._should_watch(file_path):
                            try:
                                stat = file_path.stat()
                                states[str(file_path)] = {
                                    "mtime": stat.st_mtime,
                                    "size": stat.st_size,
                                    "exists": True,
                                }
                            except (OSError, PermissionError) as e:
                                logger.warning(f"Cannot access {file_path}: {e}")
            else:
                for item in self.path.iterdir():
                    if item.is_file() and self._should_watch(item):
                        try:
                            stat = item.stat()
                            states[str(item)] = {
                                "mtime": stat.st_mtime,
                                "size": stat.st_size,
                                "exists": True,
                            }
                        except (OSError, PermissionError) as e:
                            logger.warning(f"Cannot access {item}: {e}")
        except Exception as e:
            logger.error(f"Error scanning directory: {e}")
        
        return states

    def _notify_callbacks(self, event: FileEvent) -> None:
        with self._lock:
            callbacks = self._callbacks.copy()
        
        for callback in callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Error in callback: {e}")

    def _check_changes(self) -> None:
        current_states = self._scan_directory()
        previous_paths = set(self._file_states.keys())
        current_paths = set(current_states.keys())
        
        # Deleted files
        deleted_paths = previous_paths - current_paths
        for path in deleted_paths:
            event = FileEvent(
                event_type=EventType.DELETED,
                path=path,
                is_directory=False,
                timestamp=time.time(),
            )
            self._notify_callbacks(event)
        
        # New files
        new_paths = current_paths - previous_paths
        for path in new_paths:
            event = FileEvent(
                event_type=EventType.CREATED,
                path=path,
                is_directory=False,
                timestamp=time.time(),
            )
            self._notify_callbacks(event)
        
        # Modified files
        common_paths = previous_paths & current_paths
        for path in common_paths:
            prev_state = self._file_states[path]
            curr_state = current_states[path]
            
            if (
                prev_state["mtime"] != curr_state["mtime"]
                or prev_state["size"] != curr_state["size"]
            ):
                event = FileEvent(
                    event_type=EventType.MODIFIED,
                    path=path,
                    is_directory=False,
                    timestamp=time.time(),
                )
                self._notify_callbacks(event)
        
        self._file_states = current_states

    def _watch_loop(self, interval: float) -> None:
        self._file_states = self._scan_directory()
        
        while self._running:
            try:
                time.sleep(interval)
                if self._running:
                    self._check_changes()
            except Exception as e:
                logger.error(f"Error in watch loop: {e}")
                if self._running:
                    time.sleep(interval)

    def start(self, interval: float = 1.0) -> None:
        if self._running:
            logger.warning("FileWatcher is already running")
            return
        
        self._running = True
        self._thread = threading.Thread(
            target=self._watch_loop,
            args=(interval,),
            daemon=True,
        )
        self._thread.start()
        logger.info(f"FileWatcher started monitoring: {self.path}")

    def stop(self, timeout: float = 5.0) -> None:
        if not self._running:
            logger.warning("FileWatcher is not running")
            return
        
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=timeout)
        
        logger.info("FileWatcher stopped")

    def is_running(self) -> bool:
        return self._running

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


if __name__ == "__main__":
    def on_file_event(event: FileEvent):
        print(f"[{event.event_type.value.upper()}] {event.path}")

    watcher = FileWatcher(
        path=".",
        recursive=True,
        patterns=["*.py", "*.txt"],
        ignore_patterns=["*__pycache__*", "*.pyc"],
    )
    
    watcher.add_callback(on_file_event)
    
    try:
        watcher.start(interval=0.5)
        print("Monitoring files... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        watcher.stop()