import time
import threading


class FixedWindowRateLimiter:
    """固定窗口限流器"""
    
    def __init__(self, max_requests: int, window_size: int):
        """
        初始化限流器
        
        Args:
            max_requests: 窗口内允许的最大请求数
            window_size: 窗口大小（秒）
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.current_window_start = time.time()
        self.request_count = 0
        self.lock = threading.Lock()
    
    def allow_request(self) -> bool:
        """
        检查是否允许请求
        
        Returns:
            True: 允许请求
            False: 拒绝请求（超过限流）
        """
        with self.lock:
            current_time = time.time()
            
            # 检查是否需要重置窗口
            if current_time - self.current_window_start >= self.window_size:
                self.current_window_start = current_time
                self.request_count = 0
            
            # 检查是否超过限制
            if self.request_count < self.max_requests:
                self.request_count += 1
                return True
            
            return False
    
    def get_remaining_requests(self) -> int:
        """获取当前窗口剩余请求数"""
        with self.lock:
            return max(0, self.max_requests - self.request_count)
    
    def get_time_until_reset(self) -> float:
        """获取距离窗口重置的剩余时间（秒）"""
        with self.lock:
            elapsed = time.time() - self.current_window_start
            return max(0, self.window_size - elapsed)


# 使用示例
if __name__ == "__main__":
    # 创建限流器：每秒最多5个请求
    limiter = FixedWindowRateLimiter(max_requests=5, window_size=1)
    
    # 模拟请求
    for i in range(10):
        if limiter.allow_request():
            print(f"请求 {i+1}: 通过")
        else:
            print(f"请求 {i+1}: 被限流")
        time.sleep(0.1)