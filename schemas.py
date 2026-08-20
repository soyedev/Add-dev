from pydantic import BaseModel, Field, field_validator
# Pydantic 모델을 만들기 위한 도구
# BaseModel: 데이터 모델의 기본 클래스
# Field: 각 필드의 조건, 설명, 예시를 설정
# field_validator: 특정 필드에 추가 검증 로직을 붙일 때 사용
from pydantic import BaseModel, Field, field_validator


# 출판사 정보 모델
# BookCreate 안에서 publisher 필드로 사용됨
class Publisher(BaseModel):
    # 출판사 이름
    # 최소 1글자, 최대 100글자
    name: str = Field(
        min_length=1,
        max_length=100,
        description="출판사 이름",
        examples=["한빛미디어"],
    )

    # 출판사 소재지
    # 값을 보내지 않으면 기본값은 "파주"
    city: str = Field(
        default="파주",
        description="출판사 소재지",
        examples=["파주"],
    )


# 도서 등록용 모델
# POST /books
# PUT /books/{book_id} 에서 사용
class BookCreate(BaseModel):
    # 도서 제목
    # 필수 입력이며 1~100글자만 허용
    title: str = Field(
        min_length=1,
        max_length=100,
        description="도서 제목",
        examples=["처음 시작하는 FastAPI"],
    )

    # 도서 저자
    # 필수 입력이며 1~50글자만 허용
    author: str = Field(
        min_length=1,
        max_length=50,
        description="도서 저자",
        examples=["홍길동"],
    )

    # 출판 연도
    # 1900 이상 2026 이하만 허용
    year: int = Field(
        ge=1900,
        le=2026,
        description="출판 연도",
        examples=[2024],
    )

    # 도서 태그 목록
    # 값을 보내지 않으면 빈 리스트 []가 기본값
    tags: list[str] = Field(
        default_factory=list,
        description="도서 태그 목록",
        examples=[["python", "web"]],
    )

    # 출판사 정보
    # Publisher 모델을 사용하며, 없어도 됨
    publisher: Publisher | None = Field(
        default=None,
        description="출판사 정보",
        examples=[
            {
                "name": "한빛미디어",
                "city": "서울",
            }
        ],
    )

    # title 필드에 대한 추가 검증
    # 입력된 제목의 앞뒤 공백을 제거하고,
    # 공백만 입력한 경우 오류를 발생시킴
    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("제목은 필수 입력입니다. (공백 안됨)")

        return v


# 도서 일부 수정용 모델
# PATCH /books/{book_id} 에서 사용
#
# 모든 필드가 None 가능함
# 이유: PATCH는 일부 필드만 보내도 되기 때문
class BookUpdate(BaseModel):
    # 제목을 수정할 때 사용
    # 안 보내도 되므로 기본값은 None
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="도서 제목",
    )

    # 저자를 수정할 때 사용
    author: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="도서 저자",
    )

    # 출판 연도를 수정할 때 사용
    year: int | None = Field(
        default=None,
        ge=1900,
        le=2026,
        description="출판 연도",
        examples=[2024],
    )

    # 태그 목록을 수정할 때 사용
    tags: list[str] | None = Field(
        default=None,
        description="도서 태그 목록",
        examples=[["python", "web"]],
    )

    # 출판사 정보를 수정할 때 사용
    publisher: Publisher | None = Field(
        default=None,
        description="출판사 정보",
    )


# 도서 응답용 모델
# GET /books, GET /books/{book_id}, POST /books 등의 응답에서 사용
#
# BookCreate의 모든 필드를 그대로 물려받고,
# 서버가 발급한 id만 추가함
class BookResponse(BookCreate):
    id: int = Field(
        description="도서 번호",
        examples=[1],
    )


# 날씨 응답용 모델
# GET /weather 응답에서 사용
class WeatherResponse(BaseModel):
    # 위도
    latitude: float = Field(
        description="위도",
        examples=[36.8],
    )

    # 경도
    longitude: float = Field(
        description="경도",
        examples=[127.1],
    )

    # 현재 기온
    temperature: float = Field(
        description="현재 기온(℃)",
        examples=[27.6],
    )

    # 측정 시간
    time: str = Field(
        description="측정 시간",
        examples=["2026-08-18T14:30"],
    )


# Google Books 응답용 모델
# 예전 코드에서 사용했거나, Google Books 데이터 구조를 표현할 때 사용 가능
#
# 현재 ExternalBook과 거의 같은 구조이므로,
# 실제 코드에서 사용하지 않는다면 나중에 제거해도 됨
class GoogleBooks(BaseModel):
    # 외부 API에서 가져온 도서 제목
    title: str = Field(
        description="도서 제목",
        examples=["처음 시작하는 FastAPI"],
    )

    # 외부 API에서 가져온 저자 목록
    # 저자가 없을 수도 있으므로 기본값은 빈 리스트
    authors: list[str] = Field(
        default_factory=list,
        description="저자 목록",
        examples=[["홍길동", "김철수"]],
    )

    # 외부 API에서 가져온 출판일
    # 없을 수도 있으므로 기본값은 빈 문자열
    published_date: str = Field(
        default="",
        description="출판일",
        examples=["2024-07-01"],
    )


# 외부 도서 검색 결과 모델
# GET /books/external 응답
# POST /books/from-external 요청 Body에서 사용
class ExternalBook(BaseModel):
    # 외부 API에서 가져온 도서 제목
    title: str = Field(
        description="도서 제목",
        examples=["처음 시작하는 FastAPI"],
    )

    # 외부 API에서 가져온 저자 목록
    authors: list[str] = Field(
        default_factory=list,
        description="저자 목록",
        examples=[["홍길동", "김철수"]],
    )

    # 외부 API에서 가져온 출판일
    # 예: "2024-07-01"
    # 값이 없으면 빈 문자열
    published_date: str = Field(
        default="",
        description="출판일",
        examples=["2024-07-01"],
    )