import os
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional


class MultiThreadDownloader:
    def __init__(self, url: str, output_path: str, num_threads: int = 4):
        self.url = url
        self.output_path = output_path
        self.num_threads = num_threads
        self.total_size = 0
        self.downloaded = 0
        self.lock = threading.Lock()
        
    def get_file_size(self) -> int:
        """获取文件大小"""
        response = requests.head(self.url, allow_redirects=True)
        return int(response.headers.get('content-length', 0))
    
    def download_chunk(self, start: int, end: int, chunk_id: int) -> tuple:
        """下载文件块"""
        headers = {'Range': f'bytes={start}-{end}'}
        response = requests.get(self.url, headers=headers, stream=True)
        
        chunk_path = f"{self.output_path}.part{chunk_id}"
        with open(chunk_path, 'wb') as f:
            for data in response.iter_content(chunk_size=8192):
                f.write(data)
                with self.lock:
                    self.downloaded += len(data)
        
        return chunk_id, chunk_path
    
    def merge_chunks(self, chunk_files: list):
        """合并文件块"""
        with open(self.output_path, 'wb') as output:
            for chunk_file in sorted(chunk_files):
                with open(chunk_file, 'rb') as f:
                    output.write(f.read())
                os.remove(chunk_file)
    
    def download(self, show_progress: bool = True) -> bool:
        """执行多线程下载"""
        try:
            # 获取文件大小
            self.total_size = self.get_file_size()
            if self.total_size == 0:
                print("无法获取文件大小，使用单线程下载")
                response = requests.get(self.url)
                with open(self.output_path, 'wb') as f:
                    f.write(response.content)
                return True
            
            # 计算每个线程下载的字节范围
            chunk_size = self.total_size // self.num_threads
            ranges = []
            for i in range(self.num_threads):
                start = i * chunk_size
                end = start + chunk_size - 1 if i < self.num_threads - 1 else self.total_size - 1
                ranges.append((start, end, i))
            
            # 多线程下载
            chunk_files = []
            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                futures = {executor.submit(self.download_chunk, start, end, i): i 
                          for start, end, i in ranges}
                
                for future in as_completed(futures):
                    chunk_id, chunk_path = future.result()
                    chunk_files.append(chunk_path)
                    
                    if show_progress:
                        progress = (self.downloaded / self.total_size) * 100
                        print(f"\r下载进度: {progress:.2f}%", end='')
            
            if show_progress:
                print()
            
            # 合并文件块
            self.merge_chunks(chunk_files)
            print(f"下载完成: {self.output_path}")
            return True
            
        except Exception as e:
            print(f"下载失败: {e}")
            return False


# 使用示例
if __name__ == "__main__":
    url = "https://example.com/file.zip"
    output = "downloaded_file.zip"
    
    downloader = MultiThreadDownloader(url, output, num_threads=8)
    downloader.download()