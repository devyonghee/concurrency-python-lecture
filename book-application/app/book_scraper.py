import asyncio
import aiohttp
from app.config import get_secret


class NaverBookScraper:
    NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book"
    NAVER_CLIENT_ID = get_secret('NAVER_CLIENT_ID')
    NAVER_CLIENT_SECRET = get_secret('NAVER_CLIENT_SECRET')

    @staticmethod
    def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result['items']

    def unit_url(self, keyword, start):
        return {
            "url": f"{self.NAVER_API_BOOK}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_CLIENT_ID,
                "X-Naver-Client-Secret": self.NAVER_CLIENT_SECRET
            }
        }

    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1 + i * 10) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[NaverBookScraper.fetch(session, api['url'], api['headers']) for api in apis]
            )
            print(all_data)
            result = []
            for data in all_data:
                if data is not None:
                    for book in data:
                        result.append(book)

            return result

    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))
