# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.core.tracing import init_langsmith
from app.middleware.request_logging import RequestLoggingMiddleware

logger = get_logger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan 훅
    - 앱 시작 시: 로깅 + LangSmith 초기화
    - 앱 종료 시: 필요 시 정리 작업 수행
    """
    # startup
    setup_logging()
    init_langsmith()
    logger.info("Application startup", env=settings.ENV)

    yield

    # shutdown
    logger.info("Application shutdown", env=settings.ENV)


def create_app() -> FastAPI:
    """
    앱 팩토리 함수
    - 테스트 코드, 스크립트 등에서 app 인스턴스를 재생성할 때도 사용 가능
    """
    app = FastAPI(
        title="Agent Foundation Service",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.ENV != "prod" else None,
        redoc_url="/redoc" if settings.ENV != "prod" else None,
    )

    # 자동 Request/Response 로깅 미들웨어 등록
    app.add_middleware(RequestLoggingMiddleware)

    # API 라우터 등록
    app.include_router(api_router)

    @app.get("/")
    async def root():
        return {
            "message": "Agent Foundation Service is running",
            "env": settings.ENV,
        }

    return app


# uvicorn 이 참조하는 실제 ASGI 앱 인스턴스
app = create_app()
