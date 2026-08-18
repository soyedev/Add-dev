from fastapi import FastAPI, status, HTTPException
import httpx, time
from external_api import fetch_books, fetch_books_multi, fetch_weather, load_fallback_books
from schemas import ExternalBook, WeatherResponse, BookResponse, BookCreate, GoogleBooks
from external_api import fetch_weather, fetch_books
from fastapi.staticfiles import StaticFiles

tags_metadata = [
    {"name": "도서", "description": "도서 등록, 조회, 검색"},
    {"name": "외부연동", "description": "Google Books와 날씨 API 연동"},
    {"name": "시스템", "description": "서버 상태 확인"},
]


app = FastAPI(
    title="도서 관리 API 1",
    description="도서를 등록·조회하고 외부 검색으로 정보를 가져오는 API",
    version="1.0.0",
    contact={"name": "전소예", "email": "soyeagent@gmail.com"},
    openapi_tags=tags_metadata
)

app.mount("/static", StaticFiles(directory="static"), name="static")

books = [
    {"id": 1, "title": "파이썬 입문", "author": "김철수", "year": 2021},
    {"id": 2, "title": "FastAPI 실전", "author": "이영희", "year": 2024},
    {"id": 3, "title": "파이썬 웹개발", "author": "김철수", "year": 2022},
    {"id": 4, "title": "데이터 분석 기초", "author": "박민수", "year": 2020},
    {"id": 5, "title": "FastAPI로 배우는 백엔드", "author": "이영희", "year": 2023},
]

@app.get("/", tags=["시스템"])
def read_root():
    return {"message": "Hello World!!!"}

@app.get("/health",tags=["시스템"])
def health():
    return {"status" : "ok"}

@app.get("/info",tags=["시스템"])
def info():
    return {"name": "도서관리 API", "version": "0.1.0"}

# 도서의 목록을 제공하는 엔드포인트
@app.get("/books", response_model=list[BookResponse], tags=["도서"])
def list_books():
    return books

@app.get("/books/search", tags=["도서"]) # 데코레이터 (함수에 특별한 기능이나 역할을 붙여주는 문법)
def search_books(keyword: str): #리스트 컴프리헨션

    if keyword.strip() == "":
        return []

    return [
        book
        for book in books
        if keyword.lower() in book["title"].lower()
    ]

@app.get("/books/filter", tags=["도서"])
def filter_books(keyword: str = "", sort: str = ""):
    result = books
    #for book in books:
    # 리스트 컴프리헨션 - for + if > 리스트
    result = [b for b in result if b['author'] == keyword]
    if sort == "year":
        result =sorted(result, key= lambda b: b["year"]) # 람다 인풋: 아웃풋

    return result

@app.get("/books/page", tags=["도서"])
def page_books(skip: int=0, limit: int=2):
    return books[skip: skip+limit]

@app.post("/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED, 
    tags=["도서"],
    summary="도서 등록",
    response_description="등록된 도서 정보"
    )

def create_book(book: BookCreate):
    """
    새 도서를 내 목록에 등록합니다.

    - **title**: 1자 이상 100자 이하. 앞뒤 공백은 자동 제거됩니다
    - **author**: 1자 이상 50자 이하
    - **year**: 1900 이상 2100 이하
    - **tags**: 선택. 문자열 목록
    - **publisher**: 선택. 출판사 정보

    같은 제목이 이미 있으면 409를 반환합니다.
    """
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

@app.get("/weather", response_model=WeatherResponse, tags=["외부연동"])
async def weather(latitude: float= 36.8, longitude: float=127.1):
    return await fetch_weather(latitude,longitude)

# @app.get("/books/external", response_model=list[GoogleBooks])
# async def search_external_books(keyword: str, limit: int = 5):
#     return await fetch_books(keyword, limit)

from external_api import fetch_books, fetch_weather, load_fallback_books
@app.get(
    "/books/external",
    response_model=list[ExternalBook],
    tags=["외부연동"],
    responses={
        502: {"description": "외부 API 연결 또는 서버 오류"},
        504: {"description": "외부 API 응답 시간 초과"},
    },
)
async def search_external_books(keyword: str, limit: int = 5, fallback: bool = False):
    try:
        return await fetch_books(keyword, limit)
    except httpx.TimeoutException:
        if fallback:
            return load_fallback_books()
        raise HTTPException(
    status_code=504,
    detail="외부 API 응답이 지연됩니다."
)
    except httpx.HTTPStatusError:
        if fallback:
            return load_fallback_books()
        raise HTTPException(
    status_code=502,
    detail="외부 API가 오류를 반환했습니다."
)
    except httpx.RequestError:
        if fallback:
            return load_fallback_books()
        raise HTTPException(
    status_code=502,
    detail="외부 API에 연결할 수 없습니다."
)

@app.post("/books/from-external", response_model=BookResponse, status_code=201, tags=["외부연동"])
def create_from_external(book: ExternalBook):
    for b in books:
        if b["title"] == book.title:
            raise HTTPException(status_code=409, detail="이미 등록된 제목입니다")

    year = 2000
    if book.published_date[:4].isdigit():
        year = int(book.published_date[:4])

    new_id = max([b["id"] for b in books], default=0) + 1
    new_book = {
        "id": new_id,
        "title": book.title,
        "author": book.authors[0] if book.authors else "미상",
        "year": year,
        "tags": ["외부검색"],
        "publisher": None,
    }
    books.append(new_book)
    return new_book

@app.get("/books/external/multi", tags=["외부연동"])
async def search_multi(keywords: str = "python,fastapi,django"):
    words = [w.strip() for w in keywords.split(",") if w.strip()]

    start = time.perf_counter()
    results = await fetch_books_multi(words)
    elapsed = round(time.perf_counter() - start, 2)

    return {"elapsed_seconds": elapsed, "results": results}

@app.get("/books/{book_id}", response_model=BookResponse, tags=["도서"]
         , responses={ 404 : {"description" : "해당 번호의 도서를 찾을 수 없습니다."} }) # {}=변하는 값(변수)
def read_book(book_id: int):
    for book in books:
        if book_id == book["id"]:
            return book
    #return {"error": "not found"}
    raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다.")