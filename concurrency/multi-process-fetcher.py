import requests
from concurrent.futures import ProcessPoolExecutor


def fetcher(session, url):
    with session.get(url) as response:
        return response.text


# cpu 위주의 작업을 수행한다면 multi process 를 권장
def main():
    urls = ["https://naver.com", "https://google.com", "https://instagram.com"]

    executor = ProcessPoolExecutor(max_workers=3)

    with requests.session() as session:
        results = list(executor.map(lambda url: fetcher(session, url), urls))
        print(results)


if __name__ == '__main__':
    main()
