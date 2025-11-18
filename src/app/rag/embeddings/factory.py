# src/app/rag/embeddings/factory.py
from app.rag.embeddings.base import BaseEmbedding
from app.rag.embeddings.openai_embedding import OpenAIEmbedding
from app.core.config.settings import settings


def create_embedding() -> BaseEmbedding:
    provider = settings.EMBEDDING_PROVIDER.lower()

    if provider == "openai":
        return OpenAIEmbedding()

    # 필요 시 dummy/local 등 추가
    # if provider == "dummy": ...

    raise ValueError(f"Unsupported embedding provider: {provider}")
