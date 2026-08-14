from fastapi import FastAPI, status, HTTPException
from schemas import WeatherResponse, BookResponse, BookCreate, GoogleBooks
from external_api import fetch_weather, fetch_books
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

books = [
    {"id": 1, "title": "파이썬 입문", "author": "김철수", "year": 2021},
    {"id": 2, "title": "FastAPI 실전", "author": "이영희", "year": 2024},
    {"id": 3, "title": "파이썬 웹개발", "author": "김철수", "year": 2022},
    {"id": 4, "title": "데이터 분석 기초", "author": "박민수", "year": 2020},
    {"id": 5, "title": "FastAPI로 배우는 백엔드", "author": "이영희", "year": 2023},
]

@app.get("/")
def read_root():
    return {"message": "Hello World!!!"}

@app.get("/health")
def health():
    return {"status" : "healthy"}

@app.get("/info")
def info():
    return {"name": "도서관리 API", "version": "0.1.0"}

# 도서의 목록을 제공하는 엔드포인트
@app.get("/books", response_model=list[BookResponse])
def list_books():
    return books

@app.get("/books/search") # 데코레이터 (함수에 특별한 기능이나 역할을 붙여주는 문법)
def search_books(keyword: str): #리스트 컴프리헨션

    if keyword.strip() == "":
        return []

    return [
        book
        for book in books
        if keyword.lower() in book["title"].lower()
    ]

@app.get("/books/filter")
def filter_books(keyword: str = "", sort: str = ""):
    result = books
    #for book in books:
    # 리스트 컴프리헨션 - for + if > 리스트
    result = [b for b in result if b['author'] == keyword]
    if sort == "year":
        result =sorted(result, key= lambda b: b["year"]) # 람다 인풋: 아웃풋

    return result

@app.get("/books/page")
def page_books(skip: int=0, limit: int=2):
    return books[skip: skip+limit]

@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED)

def create_book(book: BookCreate):
    for b in books:
        if b['title'] == book.title :
            raise HTTPException(status_code=409, detail='기존에 등록된 도서입니다')
        
    new_id = max([ b["id"] for b in books], default=0) + 1
    # new_book = {
    #     "id": new_id,
    #     "title": book.title,
    #     "author": book.author,
    #     "year": book.year,
    #     "tags": book.tags,
    #     "publisher": book.publisher
    # }
    new_book = {"id": new_id, **book.model_dump()} #dump는 객체를 딕셔너리로?
    books.append(new_book)

    return new_book

# @app.get("/weather/raw")
# async def weather_raw():
#     async with httpx.AsyncClient(timeout=5.0) as client:
#         response = await client.get(
#             "https://api.open-meteo.com/v1/forecast",
#             params={
#                 "latitude": 36.8,
#                 "longitude": 127.1,
#                 "current": "temperature_2m",
#             },
#         )
#         return response.json()

@app.get("/weather", response_model=WeatherResponse)
async def weather(latitude: float= 36.8, longitude: float=127.1):
    return await fetch_weather(latitude,longitude)

# 엔드포인트
@app.get("/books/external", response_model=list[GoogleBooks])
async def search_external_books(keyword: str, limit: int = 5):
    return await fetch_books(keyword, limit)

@app.get("/books/{book_id}", response_model=BookResponse) # {}=변하는 값(변수)
def read_book(book_id: int):
    for book in books:
        if book_id == book["id"]:
            return book
    #return {"error": "not found"}
    raise HTTPException(status_code=404,detail="도서를 찾을 수 없습니다.")





