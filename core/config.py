from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal, Optional
import os

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 공통
    ENV: Literal["local", "dev", "stg", "prod"] = "local"
    LOG_LEVEL: str = "INFO"

    # LLM / OpenAI 등
    LLM_PROVIDER: Literal["openai"] = "openai"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4.1-mini"

    # LangSmith / 텔레메트리
    LANGSMITH_TRACING: bool = True
    LANGSMITH_API_KEY: Optional[str] = None
    LANGSMITH_PROJECT: str = "agent-foundation"
    LANGSMITH_ENDPOINT: Optional[str] = None

    # Memory / Redis
    MEMORY_BACKEND: Literal["inmemory", "redis"] = "inmemory"
    REDIS_URL: str = "redis://localhost:6379/0"

    # RAG / Vector store
    VECTOR_STORE: Literal["chroma"] = "chroma"
    CHROMA_PERSIST_DIR: str = "./.chroma"

    # RAG 소스 설정 (문서/이미지/API)
    RAG_DOCS_DIR: str = "./data/docs"
    RAG_IMAGES_DIR: str = "./data/images"
    RAG_API_BASE_URL: Optional[str] = None

    # API 서버
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # 기타
    DEBUG: bool = Field(default=True)


settings = Settings()

if settings.OPENAI_API_KEY:
    os.environ.setdefault("OPENAI_API_KEY", settings.OPENAI_API_KEY)
