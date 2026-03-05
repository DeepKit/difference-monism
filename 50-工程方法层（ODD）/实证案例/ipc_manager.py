import multiprocessing as mp
from multiprocessing import Queue, Pipe, Manager, Value, Array
from multiprocessing.managers import BaseManager
import threading
import queue
import time
import pickle
import logging
from typing import Any, Callable, Optional, Dict, List, Tuple
from enum import Enum
import signal
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IPCMethod(Enum):
    """IPC通信方式"""
    QUEUE = "queue"
    PIPE = "pipe"
    SHARED_MEMORY = "shared_memory"
    MANAGER = "manager"


class IPCManager:
    """进程间通信管理器"""
    
    def __init__(self, method: IPCMethod = IPCMethod.QUEUE):
        self.method = method
        self.processes: Dict[str, mp.Process] = {}
        self.queues: Dict[str, Queue] = {}
        self.pipes: Dict[str, Tuple] = {}
        self.manager: Optional[Manager] = None
        self.shared_data: Dict[str, Any] = {}
        self.lock = threading.Lock()
        self._setup_signal_handlers()
        
    def _setup_signal_handlers(self):
        """设置信号处理器"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """信号处理函数"""
        logger.info(f"接收到信号 {signum}，正在清理资源...")
        self.cleanup()
        sys.exit(0)
    
    def create_queue(self, name: str, maxsize: int = 0) -> Queue:
        """创建消息队列"""
        try:
            with self.lock:
                if name in self.queues:
                    logger.warning(f"队列 {name} 已存在")
                    return self.queues[name]
                
                q = Queue(maxsize=maxsize)
                self.queues[name] = q
                logger.info(f"创建队列: {name}")
                return q
        except Exception as e:
            logger.error(f"创建队列失败: {e}")
            raise
    
    def create_pipe(self, name: str, duplex: bool = True) -> Tuple:
        """创建管道"""
        try:
            with self.lock:
                if name in self.pipes:
                    logger.warning(f"管道 {name} 已存在")
                    return self.pipes[name]
                
                conn1, conn2 = Pipe(duplex=duplex)
                self.pipes[name] = (conn1, conn2)
                logger.info(f"创建管道: {name}")
                return conn1, conn2
        except Exception as e:
            logger.error(f"创建管道失败: {e}")
            raise
    
    def create_shared_value(self, name: str, typecode: str, value: Any) -> Value:
        """创建共享值"""
        try:
            with self.lock:
                if name in self.shared_data:
                    logger.warning(f"共享值 {name} 已存在")
                    return self.shared_data[name]
                
                shared_val = Value(typecode, value)
                self.shared_data[name] = shared_val
                logger.info(f"创建共享值: {name}")
                return shared_val
        except Exception as e:
            logger.error(f"创建共享值失败: {e}")
            raise
    
    def create_shared_array(self, name: str, typecode: str, size_or_init: Any) -> Array:
        """创建共享数组"""
        try:
            with self.lock:
                if name in self.shared_data:
                    logger.warning(f"共享数组 {name} 已存在")
                    return self.shared_data[name]
                
                shared_arr = Array(typecode, size_or_init)
                self.shared_data[name] = shared_arr
                logger.info(f"创建共享数组: {name}")
                return shared_arr
        except Exception as e:
            logger.error(f"创建共享数组失败: {e}")
            raise
    
    def get_manager(self) -> Manager:
        """获取Manager对象用于共享复杂对象"""
        try:
            if self.manager is None:
                self.manager = Manager()
                logger.info("创建Manager")
            return self.manager
        except Exception as e:
            logger.error(f"创建Manager失败: {e}")
            raise
    
    def send_queue(self, queue_name: str, data: Any, timeout: Optional[float] = None) -> bool:
        """通过队列发送数据"""
        try:
            if queue_name not in self.queues:
                raise ValueError(f"队列 {queue_name} 不存在")
            
            q = self.queues[queue_name]
            if timeout:
                q.put(data, timeout=timeout)
            else:
                q.put(data)
            return True
        except queue.Full:
            logger.error(f"队列 {queue_name} 已满")
            return False
        except Exception as e:
            logger.error(f"发送数据失败: {e}")
            return False
    
    def receive_queue(self, queue_name: str, timeout: Optional[float] = None) -> Optional[Any]:
        """从队列接收数据"""
        try:
            if queue_name not in self.queues:
                raise ValueError(f"队列 {queue_name} 不存在")
            
            q = self.queues[queue_name]
            if timeout:
                return q.get(timeout=timeout)
            else:
                return q.get()
        except queue.Empty:
            logger.warning(f"队列 {queue_name} 为空")
            return None
        except Exception as e:
            logger.error(f"接收数据失败: {e}")
            return None
    
    def send_pipe(self, pipe_name: str, data: Any, conn_index: int = 0) -> bool:
        """通过管道发送数据"""
        try:
            if pipe_name not in self.pipes:
                raise ValueError(f"管道 {pipe_name} 不存在")
            
            conn = self.pipes[pipe_name][conn_index]
            conn.send(data)
            return True
        except Exception as e:
            logger.error(f"管道发送失败: {e}")
            return False
    
    def receive_pipe(self, pipe_name: str, conn_index: int = 0, timeout: Optional[float] = None) -> Optional[Any]:
        """从管道接收数据"""
        try:
            if pipe_name not in self.pipes:
                raise ValueError(f"管道 {pipe_name} 不存在")
            
            conn = self.pipes[pipe_name][conn_index]
            if timeout and conn.poll(timeout):
                return conn.recv()
            elif timeout is None:
                return conn.recv()
            return None
        except Exception as e:
            logger.error(f"管道接收失败: {e}")
            return None
    
    def start_process(self, name: str, target: Callable, args: tuple = (), kwargs: dict = None) -> bool:
        """启动进程"""
        try:
            with self.lock:
                if name in self.processes and self.processes[name].is_alive():
                    logger.warning(f"进程 {name} 已在运行")
                    return False
                
                kwargs = kwargs or {}
                process = mp.Process(target=target, args=args, kwargs=kwargs, name=name)
                process.start()
                self.processes[name] = process
                logger.info(f"启动进程: {name} (PID: {process.pid})")
                return True
        except Exception as e:
            logger.error(f"启动进程失败: {e}")
            return False
    
    def stop_process(self, name: str, timeout: float = 5.0) -> bool:
        """停止进程"""
        try:
            with self.lock:
                if name not in self.processes:
                    logger.warning(f"进程 {name} 不存在")
                    return False
                
                process = self.processes[name]
                if not process.is_alive():
                    logger.info(f"进程 {name} 已停止")
                    return True
                
                process.terminate()
                process.join(timeout=timeout)
                
                if process.is_alive():
                    logger.warning(f"进程 {name} 未响应，强制终止")
                    process.kill()
                    process.join()
                
                logger.info(f"停止进程: {name}")
                return True
        except Exception as e:
            logger.error(f"停止进程失败: {e}")
            return False
    
    def is_process_alive(self, name: str) -> bool:
        """检查进程是否存活"""
        with self.lock:
            if name in self.processes:
                return self.processes[name].is_alive()
            return False
    
    def get_process_info(self, name: str) -> Optional[Dict]:
        """获取进程信息"""
        with self.lock:
            if name not in self.processes:
                return None
            
            process = self.processes[name]
            return {
                'name': process.name,
                'pid': process.pid,
                'alive': process.is_alive(),
                'exitcode': process.exitcode
            }
    
    def broadcast_queue(self, queue_names: List[str], data: Any) -> Dict[str, bool]:
        """向多个队列广播数据"""
        results = {}
        for name in queue_names:
            results[name] = self.send_queue(name, data)
        return results
    
    def cleanup(self):
        """清理所有资源"""
        logger.info("开始清理资源...")
        
        # 停止所有进程
        with self.lock:
            for name in list(self.processes.keys()):
                self.stop_process(name)
        
        # 关闭所有管道
        for name, (conn1, conn2) in self.pipes.items():
            try:
                conn1.close()
                conn2.close()
            except Exception as e:
                logger.error(f"关闭管道 {name} 失败: {e}")
        
        # 关闭Manager
        if self.manager:
            try:
                self.manager.shutdown()
            except Exception as e:
                logger.error(f"关闭Manager失败: {e}")
        
        logger.info("资源清理完成")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.cleanup()
        return False


# 使用示例
def worker_process(queue_name: str, ipc: IPCManager):
    """工作进程示例"""
    logger.info(f"工作进程启动: {mp.current_process().name}")
    
    while True:
        try:
            data = ipc.receive_queue(queue_name, timeout=1.0)
            if data == "STOP":
                logger.info("收到停止信号")
                break
            if data:
                logger.info(f"收到数据: {data}")
                result = f"处理完成: {data}"
                ipc.send_queue(f"{queue_name}_result", result)
        except Exception as e:
            logger.error(f"工作进程错误: {e}")
            break
    
    logger.info("工作进程退出")


def pipe_worker(pipe_name: str, ipc: IPCManager, conn_index: int):
    """管道工作进程"""
    logger.info(f"管道工作进程启动: {mp.current_process().name}")
    
    while True:
        try:
            data = ipc.receive_pipe(pipe_name, conn_index, timeout=1.0)
            if data == "STOP":
                break
            if data:
                logger.info(f"管道收到: {data}")
                response = f"Echo: {data}"
                ipc.send_pipe(pipe_name, response, conn_index)
        except Exception as e:
            logger.error(f"管道工作进程错误: {e}")
            break


if __name__ == "__main__":
    # 使用上下文管理器确保资源清理
    with IPCManager() as ipc:
        # 创建队列
        ipc.create_queue("task_queue")
        ipc.create_queue("task_queue_result")
        
        # 启动工作进程
        ipc.start_process("worker1", worker_process, args=("task_queue", ipc))
        
        # 发送任务
        for i in range(5):
            ipc.send_queue("task_queue", f"任务-{i}")
            time.sleep(0.5)
        
        # 接收结果
        for i in range(5):
            result = ipc.receive_queue("task_queue_result", timeout=2.0)
            if result:
                logger.info(f"主进程收到结果: {result}")
        
        # 停止工作进程
        ipc.send_queue("task_queue", "STOP")
        time.sleep(1)
        
        # 管道示例
        conn1, conn2 = ipc.create_pipe("test_pipe")
        ipc.start_process("pipe_worker", pipe_worker, args=("test_pipe", ipc, 1))
        
        ipc.send_pipe("test_pipe", "Hello", 0)
        response = ipc.receive_pipe("test_pipe", 0, timeout=2.0)
        logger.info(f"管道响应: {response}")
        
        ipc.send_pipe("test_pipe", "STOP", 0)
        time.sleep(1)