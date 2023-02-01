import aiofiles
from aiohttp import ClientSession
import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

naver_client_id = os.getenv('NAVER_CLIENT_ID')
naver_client_secret = os.getenv('NAVER_CLIENT_SECRET')


async def image_downloader(session, image):
    image_name = image.split('/')[-1].split('?')[0]
    try:
        os.mkdir('./images')
    except FileExistsError:
        pass

    async with session.get(image) as response:
        if response.status == 200:
            async with aiofiles.open(f'./images/{image_name}', mode="wb") as file:
                await file.write(await response.read())


async def fetch(session: ClientSession, url: str):
    headers = {'X-Naver-Client-Id': naver_client_id, 'X-Naver-Client-Secret': naver_client_secret}

    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result['items']
        images = [item['link'] for item in items]
        await asyncio.gather(*[image_downloader(session, image) for image in images])


async def main():
    BASE_URL = 'https://openapi.naver.com/v1/search/image'
    keyword = 'cat'
    urls = [f"{BASE_URL}?query={keyword}&display=20&start={1 + (i * 20)}" for i in range(1)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == '__main__':
    asyncio.run(main())
