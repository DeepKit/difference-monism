import os
import threading
import requests
from pathlib import Path
from typing import Optional, Callable
from dataclasses import dataclass
import time


@dataclass
class DownloadProgress:
    """下载进度信息"""
    total_size: int
    downloaded: int
    speed: float
    percentage: float


class MultiThreadDownloader:
    """多线程下载器"""
    
    def __init__(
        self,
        url: str,
        save_path: str,
        thread_count: int = 4,
        chunk_size: int = 8192,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.url = url
        self.save_path = Path(save_path)
        self.thread_count = thread_count
        self.chunk_size = chunk_size
        self.timeout = timeout
        self.max_retries = max_retries
        
        self.total_size = 0
        self.downloaded = 0
        self.lock = threading.Lock()
        self.stop_flag = threading.Event()
        self.start_time = 0
        self.progress_callback: Optional[Callable[[DownloadProgress], None]] = None
        
    def set_progress_callback(self, callback: Callable[[DownloadProgress], None]):
        """设置进度回调函数"""
        self.progress_callback = callback
        
    def _get_file_size(self) -> int:
        """获取文件大小"""
        try:
            response = requests.head(self.url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            
            if 'Content-Length' not in response.headers:
                raise ValueError("服务器不支持获取文件大小")
                
            return int(response.headers['Content-Length'])
        except Exception as e:
            raise Exception(f"获取文件大小失败: {str(e)}")
    
    def _check_range_support(self) -> bool:
        """检查服务器是否支持断点续传"""
        try:
            headers = {'Range': 'bytes=0-0'}
            response = requests.head(self.url, headers=headers, timeout=self.timeout)
            return response.status_code == 206
        except:
            return False
    
    def _download_chunk(self, start: int, end: int, part_file: Path, thread_id: int):
        """下载文件块"""
        retries = 0
        
        while retries < self.max_retries and not self.stop_flag.is_set():
            try:
                headers = {'Range': f'bytes={start}-{end}'}
                response = requests.get(
                    self.url,
                    headers=headers,
                    stream=True,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                with open(part_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=self.chunk_size):
                        if self.stop_flag.is_set():
                            return
                            
                        if chunk:
                            f.write(chunk)
                            with self.lock:
                                self.downloaded += len(chunk)
                                self._update_progress()
                
                return
                
            except Exception as e:
                retries += 1
                if retries >= self.max_retries:
                    raise Exception(f"线程 {thread_id} 下载失败: {str(e)}")
                time.sleep(1)
    
    def _update_progress(self):
        """更新下载进度"""
        if self.progress_callback and self.total_size > 0:
            elapsed = time.time() - self.start_time
            speed = self.downloaded / elapsed if elapsed > 0 else 0
            percentage = (self.downloaded / self.total_size) * 100
            
            progress = DownloadProgress(
                total_size=self.total_size,
                downloaded=self.downloaded,
                speed=speed,
                percentage=percentage
            )
            self.progress_callback(progress)
    
    def _merge_files(self, part_files: list):
        """合并分块文件"""
        try:
            with open(self.save_path, 'wb') as output:
                for part_file in part_files:
                    with open(part_file, 'rb') as part:
                        output.write(part.read())
                    part_file.unlink()
        except Exception as e:
            raise Exception(f"合并文件失败: {str(e)}")
    
    def download(self) -> bool:
        """开始下载"""
        try:
            # 获取文件大小
            self.total_size = self._get_file_size()
            
            # 检查是否支持多线程下载
            if not self._check_range_support():
                print("服务器不支持断点续传，使用单线程下载")
                return self._single_thread_download()
            
            # 创建保存目录
            self.save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 计算每个线程下载的范围
            chunk_size = self.total_size // self.thread_count
            threads = []
            part_files = []
            
            self.start_time = time.time()
            
            for i in range(self.thread_count):
                start = i * chunk_size
                end = start + chunk_size - 1 if i < self.thread_count - 1 else self.total_size - 1
                
                part_file = self.save_path.parent / f"{self.save_path.name}.part{i}"
                part_files.append(part_file)
                
                thread = threading.Thread(
                    target=self._download_chunk,
                    args=(start, end, part_file, i)
                )
                threads.append(thread)
                thread.start()
            
            # 等待所有线程完成
            for thread in threads:
                thread.join()
            
            if self.stop_flag.is_set():
                # 清理临时文件
                for part_file in part_files:
                    if part_file.exists():
                        part_file.unlink()
                return False
            
            # 合并文件
            self._merge_files(part_files)
            
            # 验证文件大小
            if self.save_path.stat().st_size != self.total_size:
                raise Exception("下载的文件大小不匹配")
            
            return True
            
        except Exception as e:
            print(f"下载失败: {str(e)}")
            if self.save_path.exists():
                self.save_path.unlink()
            return False
    
    def _single_thread_download(self) -> bool:
        """单线程下载"""
        try:
            self.start_time = time.time()
            response = requests.get(self.url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            
            with open(self.save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if self.stop_flag.is_set():
                        return False
                        
                    if chunk:
                        f.write(chunk)
                        with self.lock:
                            self.downloaded += len(chunk)
                            self._update_progress()
            
            return True
            
        except Exception as e:
            print(f"单线程下载失败: {str(e)}")
            if self.save_path.exists():
                self.save_path.unlink()
            return False
    
    def stop(self):
        """停止下载"""
        self.stop_flag.set()


# 使用示例
if __name__ == "__main__":
    def progress_callback(progress: DownloadProgress):
        print(f"\r进度: {progress.percentage:.2f}% | "
              f"已下载: {progress.downloaded / 1024 / 1024:.2f}MB / "
              f"{progress.total_size / 1024 / 1024:.2f}MB | "
              f"速度: {progress.speed / 1024 / 1024:.2f}MB/s", end="")
    
    url = "https://example.com/file.zip"
    save_path = "downloaded_file.zip"
    
    downloader = MultiThreadDownloader(
        url=url,
        save_path=save_path,
        thread_count=8
    )
    
    downloader.set_progress_callback(progress_callback)
    
    if downloader.download():
        print("\n下载完成！")
    else:
        print("\n下载失败或被取消")