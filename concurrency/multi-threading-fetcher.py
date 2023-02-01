import requests
from concurrent.futures import ThreadPoolExecutor


def fetcher(session, url):
    with session.get(url) as response:
        return response.text


# GIL(Global Interpreter Lock) 으로 인해 멀티 스레드에서도 병렬 처리가 불가능함
def main():
    urls = ["https://naver.com", "https://google.com", "https://instagram.com"]

    executor = ThreadPoolExecutor(max_workers=3)

    with requests.session() as session:
        results = list(executor.map(lambda url: fetcher(session, url), urls))
        print(results)


if __name__ == '__main__':
    main()
