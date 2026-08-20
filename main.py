# FastAPI 앱을 만들기 위한 기본 클래스
from fastapi import FastAPI

# static 폴더 안의 HTML, CSS, JS 파일을 브라우저에서 볼 수 있게 해주는 도구
from fastapi.staticfiles import StaticFiles

# routers 폴더에서 라우터 파일들을 가져옴
# system.py   → /, /health, /info
# external.py → /weather, /books/external, /books/from-external
# books.py    → /books 관련 CRUD
from routers import system, books, external


# Swagger 문서에서 태그 그룹 설명을 보여주기 위한 설정
tags_metadata = [
    {"name": "도서", "description": "도서 등록, 조회, 검색"},
    {"name": "외부연동", "description": "Google Books와 날씨 API 연동"},
    {"name": "시스템", "description": "서버 상태 확인"},
]


# FastAPI 앱 생성
# title, description, version 등은 /docs 문서에 표시됨
app = FastAPI(
    title="도서 관리 API 1",
    description="도서를 등록·조회하고 외부 검색으로 정보를 가져오는 API",
    version="1.0.0",
    contact={"name": "전소예", "email": "soyeagent@gmail.com"},
    openapi_tags=tags_metadata,
)


# static 폴더를 웹에서 접근 가능하게 연결
# 예: static/index.html → http://127.0.0.1:8000/static/index.html
app.mount("/static", StaticFiles(directory="static"), name="static")


# 라우터 등록
# system.router: /, /health, /info
app.include_router(system.router)

# external.router를 books.router보다 먼저 등록해야 함
# 이유: /books/external 이 /books/{book_id}로 잘못 해석되는 것을 막기 위해
app.include_router(external.router)

# books.router: /books, /books/{book_id}, /books/search 등
app.include_router(books.router)
