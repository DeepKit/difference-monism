import time
import threading
from datetime import datetime
from typing import Dict, Any, Callable
from collections import deque
import json


class Sidecar:
    """边车服务类，提供辅助功能"""
    
    def __init__(self, name: str):
        self.name = name
        self.logs = deque(maxlen=1000)
        self.metrics = {}
        self.health_status = "healthy"
        self._running = False
        self._monitor_thread = None
        
    def log(self, level: str, message: str):
        """日志记录"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "sidecar": self.name
        }
        self.logs.append(log_entry)
        print(f"[{log_entry['timestamp']}] [{level}] {message}")
        
    def record_metric(self, metric_name: str, value: Any):
        """记录指标"""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append({
            "timestamp": datetime.now().isoformat(),
            "value": value
        })
        
    def get_metrics(self) -> Dict[str, Any]:
        """获取指标"""
        return self.metrics
    
    def health_check(self) -> Dict[str, str]:
        """健康检查"""
        return {
            "status": self.health_status,
            "timestamp": datetime.now().isoformat()
        }
    
    def start_monitoring(self, target_func: Callable, interval: int = 5):
        """启动监控"""
        self._running = True
        
        def monitor():
            while self._running:
                try:
                    target_func()
                    self.health_status = "healthy"
                except Exception as e:
                    self.health_status = "unhealthy"
                    self.log("ERROR", f"Monitor check failed: {str(e)}")
                time.sleep(interval)
        
        self._monitor_thread = threading.Thread(target=monitor, daemon=True)
        self._monitor_thread.start()
        self.log("INFO", "Monitoring started")
        
    def stop_monitoring(self):
        """停止监控"""
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1)
        self.log("INFO", "Monitoring stopped")


class MainApplication:
    """主应用类"""
    
    def __init__(self, name: str, sidecar: Sidecar):
        self.name = name
        self.sidecar = sidecar
        self.request_count = 0
        
    def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""
        start_time = time.time()
        
        self.sidecar.log("INFO", f"Processing request: {data}")
        
        try:
            # 模拟业务逻辑
            result = self._business_logic(data)
            self.request_count += 1
            
            # 记录指标
            duration = time.time() - start_time
            self.sidecar.record_metric("request_duration", duration)
            self.sidecar.record_metric("request_count", self.request_count)
            
            self.sidecar.log("INFO", f"Request processed successfully in {duration:.3f}s")
            return {"status": "success", "result": result}
            
        except Exception as e:
            self.sidecar.log("ERROR", f"Request failed: {str(e)}")
            self.sidecar.record_metric("error_count", 1)
            return {"status": "error", "message": str(e)}
    
    def _business_logic(self, data: Dict[str, Any]) -> Any:
        """业务逻辑"""
        time.sleep(0.1)  # 模拟处理时间
        return {"processed": data, "timestamp": datetime.now().isoformat()}
    
    def get_status(self) -> Dict[str, Any]:
        """获取应用状态"""
        return {
            "name": self.name,
            "request_count": self.request_count,
            "health": self.sidecar.health_check(),
            "metrics": self.sidecar.get_metrics()
        }


# 使用示例
if __name__ == "__main__":
    # 创建边车和主应用
    sidecar = Sidecar("app-sidecar")
    app = MainApplication("MyApp", sidecar)
    
    # 启动健康监控
    sidecar.start_monitoring(lambda: app.get_status(), interval=3)
    
    # 处理请求
    for i in range(5):
        result = app.process_request({"id": i, "data": f"request_{i}"})
        print(f"Result: {result}\n")
        time.sleep(0.5)
    
    # 获取状态
    print("\n=== Application Status ===")
    print(json.dumps(app.get_status(), indent=2))
    
    # 停止监控
    sidecar.stop_monitoring()