from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.logging import setup_logging
from core.langsmith_config import init_langsmith
from apps.api.routers import health, agents


def create_app() -> FastAPI:
    setup_logging()
    init_langsmith()

    app = FastAPI(title="Agent Foundation API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(agents.router, prefix="/agents", tags=["agents"])

    return app


app = create_app()
