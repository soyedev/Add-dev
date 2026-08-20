# 시간 측정에 사용하는 모듈
# /books/external/multi에서 여러 검색이 몇 초 걸렸는지 계산할 때 사용
import time

# 외부 API 요청 중 발생할 수 있는 오류 타입을 잡기 위해 사용
import httpx

# APIRouter: 엔드포인트를 파일별로 나누기 위한 FastAPI 도구
# HTTPException: 오류 상태 코드를 직접 반환할 때 사용
from fastapi import APIRouter, HTTPException

# books: 현재 도서 목록이 들어 있는 리스트
# save_books: 도서 목록이 바뀌었을 때 books_data.json 파일에 저장하는 함수
from database import books, save_books

# external_api.py에 따로 만들어 둔 외부 API 호출 함수들
from external_api import (
    fetch_books,          # Google Books에서 책 검색
    fetch_books_multi,    # 여러 키워드로 Google Books 동시 검색
    fetch_weather,        # 날씨 API 조회
    load_fallback_books,  # 외부 API 실패 시 사용할 예비 도서 데이터
)

# 응답과 요청 데이터의 모양을 정해 둔 Pydantic 모델
from schemas import BookResponse, ExternalBook, WeatherResponse


# 이 파일의 엔드포인트들은 Swagger 문서에서 "외부연동" 그룹으로 묶임
# prefix를 주지 않았기 때문에 아래 경로들은 전체 경로를 직접 적어야 함
router = APIRouter(tags=["외부연동"])


# 현재 날씨 조회 API
# 최종 경로: GET /weather
# latitude, longitude를 query parameter로 받아 날씨를 조회함
@router.get("/weather", response_model=WeatherResponse)
async def weather(latitude: float = 36.8, longitude: float = 127.1):
    # 실제 외부 API 호출은 external_api.py의 fetch_weather가 담당
    return await fetch_weather(latitude, longitude)


# Google Books 검색 API
# 최종 경로: GET /books/external
# 예: /books/external?keyword=fastapi&limit=5
@router.get(
    "/books/external",
    response_model=list[ExternalBook],
    responses={
        502: {"description": "외부 API 연결 또는 서버 오류"},
        504: {"description": "외부 API 응답 시간 초과"},
    },
)
async def search_external_books(
    keyword: str,             # 검색어
    limit: int = 5,           # 검색 결과 개수. 기본값은 5
    fallback: bool = False,   # 외부 API 실패 시 예비 데이터를 쓸지 여부
):
    try:
        # Google Books API에 검색 요청을 보냄
        return await fetch_books(keyword, limit)

    # 외부 API가 너무 오래 응답하지 않을 때
    except httpx.TimeoutException:
        # fallback=True이면 예비 데이터 반환
        if fallback:
            return load_fallback_books()

        # fallback=False이면 504 오류 반환
        raise HTTPException(
            status_code=504,
            detail="외부 API 응답이 지연됩니다.",
        )

    # 외부 API 서버가 4xx, 5xx 같은 오류 응답을 보냈을 때
    except httpx.HTTPStatusError:
        if fallback:
            return load_fallback_books()

        raise HTTPException(
            status_code=502,
            detail="외부 API가 오류를 반환했습니다.",
        )

    # 인터넷 연결 문제, 주소 문제 등 요청 자체가 실패했을 때
    except httpx.RequestError:
        if fallback:
            return load_fallback_books()

        raise HTTPException(
            status_code=502,
            detail="외부 API에 연결할 수 없습니다.",
        )


# 외부 검색 결과를 내 도서 목록에 저장하는 API
# 최종 경로: POST /books/from-external
#
# 사용 흐름:
# 1. GET /books/external 로 책 검색
# 2. 검색 결과 중 하나를 POST /books/from-external 로 보냄
# 3. 그 책이 내 books 목록에 저장됨
@router.post(
    "/books/from-external",
    response_model=BookResponse,
    status_code=201,
)
def create_from_external(book: ExternalBook):
    # 이미 같은 제목의 책이 있으면 중복 등록을 막음
    for b in books:
        if b["title"] == book.title:
            raise HTTPException(
                status_code=409,
                detail="이미 등록된 제목입니다",
            )

    # 외부 API의 published_date는 "2024-07-01"처럼 올 수도 있고,
    # 없거나 이상한 값일 수도 있으므로 기본 연도는 2000으로 둠
    year = 2000

    # published_date 앞 4글자가 숫자이면 연도로 사용
    # 예: "2024-07-01"[:4] -> "2024"
    if book.published_date[:4].isdigit():
        year = int(book.published_date[:4])

    # 현재 books 리스트에서 가장 큰 id를 찾고, 거기에 1을 더해 새 id 생성
    # books가 비어 있으면 default=0 덕분에 새 id는 1이 됨
    new_id = max([b["id"] for b in books], default=0) + 1

    # ExternalBook 형식을 내부 BookResponse 형식에 맞게 변환
    new_book = {
        "id": new_id,
        "title": book.title,
        "author": book.authors[0] if book.authors else "미상",
        "year": year,
        "tags": ["외부검색"],
        "publisher": None,
    }

    # 메모리의 books 리스트에 새 도서 추가
    books.append(new_book)

    # books_data.json 파일에도 저장
    # 이걸 해야 서버를 껐다 켜도 데이터가 남아 있음
    save_books()

    # 등록된 도서 반환
    return new_book


# 여러 키워드로 Google Books를 동시에 검색하는 API
# 최종 경로: GET /books/external/multi
# 예: /books/external/multi?keywords=python,fastapi,django
@router.get("/books/external/multi")
async def search_multi(keywords: str = "python,fastapi,django"):
    # "python,fastapi,django" 문자열을 쉼표 기준으로 나눔
    # strip()으로 앞뒤 공백 제거
    # 빈 문자열은 제외
    words = [w.strip() for w in keywords.split(",") if w.strip()]

    # 검색 시작 시간 기록
    start = time.perf_counter()

    # 여러 키워드 검색 실행
    results = await fetch_books_multi(words)

    # 걸린 시간 계산
    elapsed = round(time.perf_counter() - start, 2)

    # 검색 결과와 걸린 시간을 함께 반환
    return {
        "elapsed_seconds": elapsed,
        "results": results,
    }