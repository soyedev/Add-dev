from pydantic import BaseModel, Field, field_validator

class Publisher(BaseModel):
    name: str = Field(min_length=1, max_length=100,
                description="출판사 이름",
                examples=["한빛미디어"]
            )
    city: str = Field(default="파주",
                description="출판사 소재지",
                examples=["파주"]
            )

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100,
        description="도서 제목",
        examples=["처음 시작하는 FastAPI"],)
    author: str = Field(min_length=1, max_length=50,
        description="도서 저자",
        examples=["홍길동",])
    year: int = Field(ge=1900, le=2026,
        description="출판 연도",
        examples=["2024"],)
    tags: list[str] = Field(default_factory=list,
        description="도서 태그 목록",
        examples=["python","web"])
    publisher: Publisher | None = Field(
        default=None,
        description="출판사 정보",
        examples=[
        {
            "name": "한빛미디어",
            "city": "서울"
        }
    ]
)

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        v = v.strip()

        # 공백 문자열 체크
        if not v:
            raise ValueError("제목은 필수 입력입니다. (공백 안됨)")

        return v

class BookResponse(BookCreate):
    id: int

class WeatherResponse(BaseModel):
    latitude: float = Field(
        description="위도",
        examples=[36.8]
    )
    longitude: float = Field(
        description="경도",
        examples=[127.1]
    )
    temperature: float = Field(
        description="현재 기온(℃)",
        examples=[27.6]
    )
    time: str = Field(
        description="측정 시간",
        examples=["2026-08-18T14:30"]
    )


class GoogleBooks(BaseModel):
    title: str = Field(
        description="도서 제목",
        examples=["처음 시작하는 FastAPI"]
    )
    authors: list[str] = Field(
        default_factory=list,
        description="저자 목록",
        examples=[["홍길동", "김철수"]]
    )
    published_date: str = Field(
        default="",
        description="출판일",
        examples=["2024-07-01"]
    )


class ExternalBook(BaseModel):
    title: str = Field(
        description="도서 제목",
        examples=["처음 시작하는 FastAPI"]
    )
    authors: list[str] = Field(
        default_factory=list,
        description="저자 목록",
        examples=[["홍길동", "김철수"]]
    )
    published_date: str = Field(
        default="",
        description="출판일",
        examples=["2024-07-01"]
    )