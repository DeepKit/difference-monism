import asyncio
import aiohttp
from aiohttp import ClientSession, ClientTimeout
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import Set, List, Dict, Optional, Callable
import logging
from dataclasses import dataclass
from datetime import datetime
import time
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CrawlResult:
    url: str
    status_code: int
    content: str
    links: List[str]
    timestamp: datetime
    error: Optional[str] = None


class AsyncWebCrawler:
    def __init__(
        self,
        max_concurrent: int = 10,
        timeout: int = 30,
        max_retries: int = 3,
        delay: float = 0.5,
        max_depth: int = 3,
        respect_robots: bool = True,
        user_agent: str = "AsyncWebCrawler/1.0"
    ):
        self.max_concurrent = max_concurrent
        self.timeout = ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self.delay = delay
        self.max_depth = max_depth
        self.respect_robots = respect_robots
        self.user_agent = user_agent
        
        self.visited_urls: Set[str] = set()
        self.failed_urls: Dict[str, str] = {}
        self.results: List[CrawlResult] = []
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session: Optional[ClientSession] = None
        self.queue: deque = deque()
        self.robots_cache: Dict[str, bool] = {}
        
    async def __aenter__(self):
        await self.start()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def start(self):
        headers = {"User-Agent": self.user_agent}
        self.session = ClientSession(
            timeout=self.timeout,
            headers=headers
        )
        
    async def close(self):
        if self.session:
            await self.session.close()
            
    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
    def is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
            
    def get_domain(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
        
    async def check_robots_txt(self, url: str) -> bool:
        if not self.respect_robots:
            return True
            
        domain = self.get_domain(url)
        
        if domain in self.robots_cache:
            return self.robots_cache[domain]
            
        robots_url = f"{domain}/robots.txt"
        try:
            async with self.session.get(robots_url) as response:
                if response.status == 200:
                    content = await response.text()
                    self.robots_cache[domain] = "Disallow: /" not in content
                else:
                    self.robots_cache[domain] = True
        except Exception:
            self.robots_cache[domain] = True
            
        return self.robots_cache[domain]
        
    async def fetch_url(self, url: str, retry_count: int = 0) -> Optional[CrawlResult]:
        try:
            async with self.semaphore:
                await asyncio.sleep(self.delay)
                
                if not await self.check_robots_txt(url):
                    logger.warning(f"Blocked by robots.txt: {url}")
                    return None
                    
                async with self.session.get(url, allow_redirects=True) as response:
                    content = await response.text()
                    
                    links = []
                    if response.status == 200:
                        links = self.extract_links(content, url)
                        
                    result = CrawlResult(
                        url=url,
                        status_code=response.status,
                        content=content,
                        links=links,
                        timestamp=datetime.now()
                    )
                    
                    logger.info(f"Successfully crawled: {url} (Status: {response.status})")
                    return result
                    
        except asyncio.TimeoutError:
            error_msg = f"Timeout error for {url}"
            logger.error(error_msg)
            if retry_count < self.max_retries:
                logger.info(f"Retrying {url} (attempt {retry_count + 1}/{self.max_retries})")
                await asyncio.sleep(2 ** retry_count)
                return await self.fetch_url(url, retry_count + 1)
            return CrawlResult(url=url, status_code=0, content="", links=[], 
                             timestamp=datetime.now(), error=error_msg)
                             
        except aiohttp.ClientError as e:
            error_msg = f"Client error for {url}: {str(e)}"
            logger.error(error_msg)
            if retry_count < self.max_retries:
                logger.info(f"Retrying {url} (attempt {retry_count + 1}/{self.max_retries})")
                await asyncio.sleep(2 ** retry_count)
                return await self.fetch_url(url, retry_count + 1)
            return CrawlResult(url=url, status_code=0, content="", links=[], 
                             timestamp=datetime.now(), error=error_msg)
                             
        except Exception as e:
            error_msg = f"Unexpected error for {url}: {str(e)}"
            logger.error(error_msg)
            return CrawlResult(url=url, status_code=0, content="", links=[], 
                             timestamp=datetime.now(), error=error_msg)
                             
    def extract_links(self, html: str, base_url: str) -> List[str]:
        links = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']
                absolute_url = urljoin(base_url, href)
                
                if self.is_valid_url(absolute_url):
                    normalized = self.normalize_url(absolute_url)
                    links.append(normalized)
                    
        except Exception as e:
            logger.error(f"Error extracting links from {base_url}: {str(e)}")
            
        return links
        
    async def crawl_url(self, url: str, depth: int = 0):
        if depth > self.max_depth:
            return
            
        normalized_url = self.normalize_url(url)
        
        if normalized_url in self.visited_urls:
            return
            
        self.visited_urls.add(normalized_url)
        
        result = await self.fetch_url(normalized_url)
        
        if result:
            self.results.append(result)
            
            if result.error:
                self.failed_urls[normalized_url] = result.error
            elif result.status_code == 200 and depth < self.max_depth:
                for link in result.links:
                    if link not in self.visited_urls:
                        self.queue.append((link, depth + 1))
                        
    async def crawl(self, start_urls: List[str], callback: Optional[Callable] = None) -> List[CrawlResult]:
        if not self.session:
            await self.start()
            
        for url in start_urls:
            self.queue.append((url, 0))
            
        tasks = []
        
        while self.queue or tasks:
            while self.queue and len(tasks) < self.max_concurrent:
                url, depth = self.queue.popleft()
                task = asyncio.create_task(self.crawl_url(url, depth))
                tasks.append(task)
                
            if tasks:
                done, tasks = await asyncio.wait(
                    tasks, 
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                if callback:
                    for task in done:
                        try:
                            await task
                            if self.results:
                                callback(self.results[-1])
                        except Exception as e:
                            logger.error(f"Task error: {str(e)}")
                            
        return self.results
        
    def get_statistics(self) -> Dict:
        return {
            "total_crawled": len(self.visited_urls),
            "successful": len([r for r in self.results if not r.error]),
            "failed": len(self.failed_urls),
            "total_results": len(self.results)
        }


async def main():
    start_urls = [
        "https://example.com",
    ]
    
    def on_result(result: CrawlResult):
        print(f"Crawled: {result.url} - Status: {result.status_code}")
    
    async with AsyncWebCrawler(
        max_concurrent=5,
        timeout=30,
        max_depth=2,
        delay=1.0
    ) as crawler:
        results = await crawler.crawl(start_urls, callback=on_result)
        
        print("\n=== Statistics ===")
        stats = crawler.get_statistics()
        for key, value in stats.items():
            print(f"{key}: {value}")
            
        print("\n=== Failed URLs ===")
        for url, error in crawler.failed_urls.items():
            print(f"{url}: {error}")


if __name__ == "__main__":
    asyncio.run(main())