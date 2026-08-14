# FastAPI 도서 관리 API

## 프로젝트 소개

FastAPI와 HTML, JavaScript(Fetch API)를 이용하여 구현한 도서 관리 프로젝트입니다.

REST API를 활용하여 도서 조회, 검색, 등록, 검증 기능을 구현하였으며,
HTML 페이지와 Fetch API를 통해 서버와 통신합니다.

또한 Open-Meteo API와 Google Books API를 연동하여 외부 API 호출과 비동기(Async) 처리 했습니다.

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

---

## 실행 방법

```bash
fastapi dev main.py
```

브라우저 접속

```
http://127.0.0.1:8000/static/index.html
```

또는 Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 화면 구성

- 01. 서버 상태 확인
- 02. 도서 목록 조회
- 03. 도서 단건 조회
- 04. 도서 검색
- 05. 저자 필터 및 정렬
- 06. 페이지네이션
- 07. 도서 등록
- 08. 입력 검증
- 09. 등록 후 목록 갱신
- 10. 404 예외 처리
- 11. 태그 및 출판사 등록
- 12. 상태 코드 통합 처리
- 13. 등록 + 검색 통합 화면
- 14. 현재 날씨 조회(Open-Meteo API)
- 15. Google Books API 도서 검색
