# app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal, Optional
import os

def get_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Project root not found.")

BASE_DIR = get_project_root()

# 예: RAG 리소스, config 파일 등
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 환경
    ENV: Literal["local", "dev", "stg", "prod"] = "local"
    LOG_LEVEL: str = "INFO"

    # LLM / OpenAI
    LLM_PROVIDER: Literal[
        "openai",
        "gemini",
        "anthropic",
        "azure_openai",
        "ollama",
    ] = "openai"

    # OpanAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4.1-mini"

    # Gemini (Google)
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None

    # Azure OpenAI
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_DEPLOYMENT: Optional[str] = None

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # LangSmith (옵션)
    LANGSMITH_TRACING: bool = True
    LANGSMITH_API_KEY: Optional[str] = None
    LANGSMITH_PROJECT: str = "agent-foundation"
    LANGSMITH_ENDPOINT: Optional[str] = None

    # Memory / Redis
    MEMORY_BACKEND: Literal["inmemory", "redis"] = "inmemory"
    REDIS_URL: str = "redis://localhost:6379/0"

    # RAG / Vector DB 예시
    VECTOR_STORE_BACKEND: Literal["chroma", "pgvector", "inmemory"] = "inmemory"

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

