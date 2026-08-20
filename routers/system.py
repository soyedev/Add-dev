# APIRouter는 엔드포인트를 파일별로 나누기 위해 사용하는 FastAPI 도구
from fastapi import APIRouter


# 이 파일의 엔드포인트들은 Swagger 문서에서 "시스템" 그룹으로 묶임
router = APIRouter(tags=["시스템"])


# 루트 경로
# 최종 경로: GET /
# 서버가 정상적으로 응답하는지 간단히 확인할 때 사용
@router.get("/", summary="루트")
def read_root():
    return {"message": "Hello World!!!"}


# 서버 상태 확인
# 최종 경로: GET /health
# 서버가 살아 있는지 확인할 때 사용
@router.get("/health", summary="서버 상태 확인")
def health():
    return {"status": "ok"}


# 앱 정보 확인
# 최종 경로: GET /info
# API 이름과 버전 정보를 반환
@router.get("/info", summary="앱 정보")
def info():
    return {"name": "도서관리 API", "version": "0.1.0"}