from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.Book import BookModel
from app.book_scraper import NaverBookScraper

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "콜렉터 북북이"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    keyword = q
    if not keyword:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, 'title': '콜렉터 북북이'}
        )
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        book_models = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "콜렉터 북북이", "books": book_models}
        )
    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, 10)
    book_models = []
    for book in books:
        book_model = BookModel(keyword=keyword,
                               publisher=book['publisher'],
                               price=book['discount'],
                               image=book['image'])
        book_models.append(book_model)
    await mongodb.engine.save_all(book_models)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "콜렉터 북북이", "books": book_models}
    )


@app.on_event('startup')
def on_app_start():
    mongodb.connect()


@app.on_event('shutdown')
def on_app_shutdown():
    mongodb.disconnect()
