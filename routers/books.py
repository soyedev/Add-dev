# FastAPI에서 라우터, 에러 처리, 상태 코드를 가져옴
# APIRouter: 엔드포인트를 파일별로 나눌 때 사용
# HTTPException: 404, 409 같은 오류 응답을 직접 발생시킬 때 사용
# status: 201_CREATED 같은 상태 코드를 이름으로 쓰기 위해 사용
from fastapi import APIRouter, HTTPException, status

# database.py에서 도서 목록과 저장 함수를 가져옴
# books: 현재 도서 목록이 들어 있는 리스트
# save_books: books 리스트 내용을 books_data.json 파일에 저장하는 함수
from database import books, save_books

# schemas.py에서 요청/응답 데이터 모델을 가져옴
# BookCreate: 도서 등록/전체 수정 때 사용하는 모델
# BookUpdate: 도서 일부 수정 때 사용하는 모델
# BookResponse: 응답으로 내보낼 도서 모델
from schemas import BookUpdate, BookResponse, BookCreate


# 이 파일의 모든 경로 앞에는 /books가 자동으로 붙음
# 예: @router.get("")          -> GET /books
# 예: @router.get("/{book_id}") -> GET /books/{book_id}
router = APIRouter(prefix="/books", tags=["도서"])


# 도서 id로 책 한 권을 찾는 공통 함수
# 여러 엔드포인트에서 같은 조회 코드가 반복되므로 함수로 분리함
def get_book_or_404(book_id: int) -> dict:
    # books 리스트를 하나씩 돌면서 id가 같은 책을 찾음
    for b in books:
        if b["id"] == book_id:
            return b

    # 반복문이 끝날 때까지 못 찾으면 404 오류 발생
    raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다")


# 도서 목록 조회
# 최종 경로: GET /books
@router.get("", response_model=list[BookResponse])
def list_books():
    # 현재 books 리스트 전체를 반환
    return books


# 도서 제목 검색
# 최종 경로: GET /books/search?keyword=검색어
@router.get("/search")
def search_books(keyword: str):
    # 검색어가 빈 문자열이거나 공백만 있으면 빈 리스트 반환
    if keyword.strip() == "":
        return []

    # 제목에 keyword가 포함된 책만 골라서 반환
    # lower()를 사용해서 대소문자를 구분하지 않고 검색
    return [
        book
        for book in books
        if keyword.lower() in book["title"].lower()
    ]


# 저자 필터, 연도 정렬
# 최종 경로 예시:
# GET /books/filter?keyword=김철수
# GET /books/filter?keyword=김철수&sort=year
@router.get("/filter")
def filter_books(keyword: str = "", sort: str = ""):
    # 처음에는 전체 도서 목록에서 시작
    result = books

    # keyword가 있으면 author가 keyword와 같은 책만 남김
    if keyword.strip():
        result = [b for b in result if b["author"] == keyword]

    # sort가 year이면 연도 기준 오름차순 정렬
    if sort == "year":
        result = sorted(result, key=lambda b: b["year"])

    return result


# 페이지네이션
# 최종 경로 예시: GET /books/page?skip=0&limit=2
@router.get("/page")
def page_books(skip: int = 0, limit: int = 2):
    # skip개를 건너뛰고 limit개만 반환
    return books[skip: skip + limit]


# 도서 등록
# 최종 경로: POST /books
@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="도서 등록",
    response_description="등록된 도서 정보",
)
def create_book(book: BookCreate):
    """
    새 도서를 내 목록에 등록합니다.

    - title: 도서 제목
    - author: 저자
    - year: 출판 연도
    - tags: 선택 입력
    - publisher: 선택 입력

    같은 제목이 이미 있으면 409 오류를 반환합니다.
    """

    # 같은 제목의 책이 이미 있는지 검사
    for b in books:
        if b["title"] == book.title:
            raise HTTPException(
                status_code=409,
                detail="기존에 등록된 도서입니다",
            )

    # 기존 id 중 가장 큰 값에 1을 더해서 새 id 생성
    # books가 비어 있으면 default=0 덕분에 새 id는 1이 됨
    new_id = max([b["id"] for b in books], default=0) + 1

    # Pydantic 모델인 book을 딕셔너리로 바꾸고 id를 추가
    new_book = {"id": new_id, **book.model_dump()}

    # 메모리의 books 리스트에 새 책 추가
    books.append(new_book)

    # books_data.json 파일에도 저장
    # 이걸 해야 서버를 껐다 켜도 등록한 책이 남아 있음
    save_books()

    return new_book


# 도서 전체 수정
# 최종 경로: PUT /books/{book_id}
# PUT은 전체 교체이므로 title, author, year 같은 필수 필드를 모두 보내야 함
@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="도서 전체 수정",
    responses={404: {"description": "해당 번호의 도서가 없습니다"}},
)
def update_book(book_id: int, book: BookCreate):
    """
    도서 정보를 전체 교체합니다.
    일부 필드만 수정하고 싶다면 PATCH를 사용합니다.
    """

    # 수정할 기존 도서를 찾음
    # 없으면 get_book_or_404 함수 안에서 404 오류 발생
    old_book = get_book_or_404(book_id)

    # 기존 id는 유지하고, 나머지 정보는 새 요청 데이터로 교체
    new_book = {"id": book_id, **book.model_dump()}

    # old_book이 books 리스트의 몇 번째 위치에 있는지 찾고,
    # 그 자리에 new_book을 넣어 전체 교체
    books[books.index(old_book)] = new_book

    # 변경된 내용을 파일에 저장
    save_books()

    return new_book


# 도서 일부 수정
# 최종 경로: PATCH /books/{book_id}
# PATCH는 보낸 필드만 수정함
@router.patch(
    "/{book_id}",
    response_model=BookResponse,
    summary="도서 일부 정보 수정",
    responses={404: {"description": "해당 번호의 도서가 없습니다"}},
)
def patch_book(book_id: int, patch: BookUpdate):
    """
    도서 정보를 일부만 수정합니다.
    전체 교체가 필요하면 PUT을 사용합니다.
    """

    # 수정할 기존 도서를 찾음
    book = get_book_or_404(book_id)

    # exclude_unset=True:
    # 요청에서 실제로 보낸 필드만 딕셔너리로 만듦
    # 이 옵션이 없으면 보내지 않은 필드가 None으로 들어가 기존 값을 지울 수 있음
    changes = patch.model_dump(exclude_unset=True)

    # 기존 책 딕셔너리에 변경된 필드만 덮어씀
    book.update(changes)

    # 변경된 내용을 파일에 저장
    save_books()

    return book


# 도서 삭제
# 최종 경로: DELETE /books/{book_id}
# 삭제 성공 시 204 No Content를 반환하므로 응답 본문은 없음
@router.delete(
    "/{book_id}",
    status_code=204,
    summary="도서 삭제",
    responses={404: {"description": "해당 번호의 도서가 없습니다"}},
)
def delete_book(book_id: int):
    # 삭제할 도서를 찾음
    book = get_book_or_404(book_id)

    # 전체 books 리스트에서 해당 책을 제거
    books.remove(book)

    # 삭제 결과를 파일에 저장
    save_books()

    # 204 No Content에서는 본문을 보내지 않음
    return None


# 도서 단건 조회
# 최종 경로: GET /books/{book_id}
#
# 중요:
# /search, /filter, /page 같은 고정 경로보다 아래에 있어야 함
# 위에 있으면 "search"를 book_id로 착각해서 오류가 날 수 있음
@router.get(
    "/{book_id}",
    response_model=BookResponse,
    responses={404: {"description": "해당 번호의 도서를 찾을 수 없습니다."}},
)
def read_book(book_id: int):
    return get_book_or_404(book_id)