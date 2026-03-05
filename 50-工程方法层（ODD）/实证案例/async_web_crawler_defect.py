import asyncio
import aiohttp
from typing import List, Set, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


class AsyncWebCrawler:
    def __init__(self, max_concurrent: int = 10, timeout: int = 30):
        self.max_concurrent = max_concurrent
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.visited: Set[str] = set()
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """获取单个URL的内容"""
        if url in self.visited:
            return None
            
        self.visited.add(url)
        
        async with self.semaphore:
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        return await response.text()
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return None
    
    async def parse_links(self, html: str, base_url: str) -> List[str]:
        """从HTML中提取链接"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(base_url, link['href'])
            if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                links.append(absolute_url)
        
        return links
    
    async def crawl(self, start_url: str, max_pages: int = 50) -> List[dict]:
        """爬取网站"""
        results = []
        to_visit = [start_url]
        
        async with aiohttp.ClientSession() as session:
            while to_visit and len(results) < max_pages:
                tasks = []
                batch = to_visit[:self.max_concurrent]
                to_visit = to_visit[self.max_concurrent:]
                
                for url in batch:
                    tasks.append(self.fetch(session, url))
                
                pages = await asyncio.gather(*tasks)
                
                for url, html in zip(batch, pages):
                    if html:
                        results.append({'url': url, 'content': html})
                        links = await self.parse_links(html, url)
                        to_visit.extend([link for link in links if link not in self.visited])
        
        return results


# 使用示例
async def main():
    crawler = AsyncWebCrawler(max_concurrent=5)
    results = await crawler.crawl('https://example.com', max_pages=10)
    print(f"爬取了 {len(results)} 个页面")
    for result in results:
        print(f"URL: {result['url']}, 内容长度: {len(result['content'])}")


if __name__ == '__main__':
    asyncio.run(main())