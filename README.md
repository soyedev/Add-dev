# FastAPI 도서 관리 API

## 프로젝트 소개

FastAPI와 HTML, JavaScript(Fetch API)를 이용하여 구현한 도서 관리 프로젝트입니다.

REST API를 활용하여 도서 조회, 검색, 등록, 수정, 삭제 기능을 구현하였으며, HTML 페이지와 Fetch API를 통해 서버와 통신합니다.

또한 Open-Meteo API와 Google Books API를 연동하여 외부 API 호출과 비동기(Async) 처리를 구현하였고, Swagger(OpenAPI)를 이용한 API 문서화와 Postman을 이용한 API 테스트 환경을 구성했습니다.

5일차에는 CRUD 기능을 완성하고, 데이터를 JSON 파일에 저장하여 서버를 재시작해도 데이터가 유지되도록 개선했습니다. 또한 `APIRouter`를 이용해 기능별로 라우터를 분리하여 코드 구조를 정리했습니다.

---

## 구현 기능

### 조회 기능

- 서버 상태 확인
- 앱 정보 조회
- 도서 목록 조회
- 도서 단건 조회
- 도서 제목 검색
- 저자별 필터링
- 연도순 정렬
- 페이지네이션

### 등록 기능

- 도서 등록
- 등록 후 목록 자동 갱신
- 입력값 검증(Pydantic)
- 404 예외 처리
- 409 중복 등록 처리
- 외부 검색 결과를 내 도서 목록에 등록

### 수정 및 삭제 기능

- `PUT`을 이용한 도서 전체 수정
- `PATCH`를 이용한 도서 일부 수정
- `DELETE`를 이용한 도서 삭제
- 삭제 성공 시 `204 No Content` 반환
- `get_book_or_404()` 공통 함수로 중복 조회 코드 제거
- 수정·삭제 후 JSON 파일에 변경 사항 저장

### 데이터 저장 기능

- `database.py`를 이용한 데이터 관리
- `books_data.json` 파일을 통한 데이터 영속화
- 서버 시작 시 저장된 도서 데이터 불러오기
- 데이터 변경 시 `save_books()`로 파일 저장
- `.gitignore`에 데이터 파일 등록

### 추가 기능

- 태그(tags) 등록
- 출판사(Publisher) 정보 등록
- 중첩 모델(Nested Model) 사용
- 입력창 초기화
- 등록 버튼 중복 클릭 방지
- 등록 화면과 검색 화면 통합
- 통합 관리 화면에서 등록·수정·삭제 처리

### 외부 API 연동

- Open-Meteo API를 이용한 현재 날씨 조회
- Google Books API를 이용한 도서 검색
- 여러 키워드를 동시에 검색하는 외부 도서 검색 기능
- HTTPX AsyncClient를 이용한 비동기 API 호출
- 환경 변수(.env)를 이용한 API Key 관리
- Fallback 데이터를 이용한 예외 처리
- 외부 검색 결과를 내부 도서 목록에 저장

### API 문서화 및 테스트

- Swagger(OpenAPI) 문서화
- tags를 이용한 API 분류
- summary 및 독스트링 작성
- responses를 이용한 오류 응답 문서화
- Pydantic 모델 description 및 examples 작성
- Postman Collection 구성
- Environment(baseUrl) 설정
- Pre-request Script 작성
- Post-response Script를 이용한 응답 자동 검증

### 코드 구조 정리

- `main.py`를 앱 생성과 라우터 등록 중심으로 정리
- `routers/books.py`로 도서 CRUD 기능 분리
- `routers/external.py`로 외부 API 연동 기능 분리
- `routers/system.py`로 시스템 상태 확인 기능 분리
- `database.py`로 데이터 저장과 불러오기 기능 분리
- `schemas.py`로 Pydantic 모델 관리
- 순환 import를 피하기 위한 파일 구조 정리

---

## 사용 기술

- Python
- FastAPI
- Pydantic
- HTTPX
- Requests
- python-dotenv
- HTML5
- JavaScript (Fetch API)
- Swagger (OpenAPI)
- Postman
- Git / GitHub
- JSON 파일 저장
- APIRouter

---

## 프로젝트 구조

```text
01-fastapi-basic/
├── main.py
├── database.py
├── schemas.py
├── external_api.py
├── books_data.json
├── sample_books.json
├── .env
├── .gitignore
├── routers/
│   ├── __init__.py
│   ├── system.py
│   ├── books.py
│   └── external.py
└── static/
    ├── index.html
    ├── 20-edit.html
    └── 21-manage.html
```

---

## 실행 방법

### 서버 실행

```bash
fastapi dev main.py
```

### 웹 페이지

```text
http://127.0.0.1:8000/static/index.html
```

### 통합 관리 화면

```text
http://127.0.0.1:8000/static/21-manage.html
```

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## 주요 API

| Method | Endpoint | 설명 |
| ------ | -------- | ---- |
| GET | `/` | 루트 경로 |
| GET | `/health` | 서버 상태 확인 |
| GET | `/info` | 앱 정보 조회 |
| GET | `/books` | 도서 목록 조회 |
| POST | `/books` | 도서 등록 |
| GET | `/books/{book_id}` | 도서 단건 조회 |
| PUT | `/books/{book_id}` | 도서 전체 수정 |
| PATCH | `/books/{book_id}` | 도서 일부 수정 |
| DELETE | `/books/{book_id}` | 도서 삭제 |
| GET | `/books/search` | 도서 제목 검색 |
| GET | `/books/filter` | 저자 필터 및 연도 정렬 |
| GET | `/books/page` | 페이지네이션 |
| GET | `/weather` | 현재 날씨 조회 |
| GET | `/books/external` | Google Books 검색 |
| GET | `/books/external/multi` | 여러 키워드 외부 도서 검색 |
| POST | `/books/from-external` | 외부 도서 등록 |

---

## CRUD 동작 정리

| 기능 | Method | Endpoint | 설명 |
| ---- | ------ | -------- | ---- |
| Create | POST | `/books` | 새 도서 등록 |
| Read | GET | `/books`, `/books/{book_id}` | 도서 목록 및 단건 조회 |
| Update | PUT | `/books/{book_id}` | 도서 전체 수정 |
| Update | PATCH | `/books/{book_id}` | 도서 일부 수정 |
| Delete | DELETE | `/books/{book_id}` | 도서 삭제 |

---
