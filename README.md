# FastAPI 도서 관리 API

## 프로젝트 소개

FastAPI와 HTML, JavaScript(Fetch API)를 이용하여 구현한 도서 관리 프로젝트입니다.

REST API를 활용하여 도서 조회, 검색, 등록, 검증 기능을 구현하였으며, HTML 페이지와 Fetch API를 통해 서버와 통신합니다.

또한 Open-Meteo API와 Google Books API를 연동하여 외부 API 호출과 비동기(Async) 처리를 구현하였으며, Swagger(OpenAPI)를 이용한 API 문서화와 Postman을 이용한 API 테스트 환경을 구성했습니다.

---

## 구현 기능

### 조회 기능

- 서버 상태 확인
- 도서 목록 조회
- 도서 단건 조회
- 도서 검색
- 저자별 필터링
- 연도순 정렬
- 페이지네이션

### 등록 기능

- 도서 등록
- 등록 후 목록 자동 갱신
- 입력값 검증(Pydantic)
- 404 예외 처리
- 409 중복 등록 처리

### 추가 기능

- 태그(tags) 등록
- 출판사(Publisher) 정보 등록
- 중첩 모델(Nested Model) 사용
- 입력창 초기화
- 등록 버튼 중복 클릭 방지
- 등록 화면과 검색 화면 통합

### 외부 API 연동

- Open-Meteo API를 이용한 현재 날씨 조회
- Google Books API를 이용한 도서 검색
- HTTPX AsyncClient를 이용한 비동기 API 호출
- 환경 변수(.env)를 이용한 API Key 관리
- Fallback 데이터를 이용한 예외 처리

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

---

## 실행 방법

### 서버 실행

```bash
fastapi dev main.py
```

### 웹 페이지

```
http://127.0.0.1:8000/static/index.html
```

### Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 주요 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/health` | 서버 상태 확인 |
| GET | `/books` | 도서 목록 조회 |
| GET | `/books/{book_id}` | 도서 단건 조회 |
| GET | `/books/search` | 도서 검색 |
| GET | `/books/filter` | 저자 필터 및 정렬 |
| GET | `/books/page` | 페이지네이션 |
| POST | `/books` | 도서 등록 |
| GET | `/weather` | 현재 날씨 조회 |
| GET | `/books/external` | Google Books 검색 |
| POST | `/books/from-external` | 외부 도서 등록 |

---