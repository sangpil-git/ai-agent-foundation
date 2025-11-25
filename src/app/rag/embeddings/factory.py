# src/app/rag/embeddings/factory.py
from __future__ import annotations

from typing import Literal

from app.rag.embeddings.base import BaseEmbedding
from app.rag.embeddings.openai_embedding import OpenAIEmbedding
from app.core.config.settings import settings


EmbeddingBackend = Literal["openai"]  # 나중에 "upstage", "huggingface" 등 추가


def create_embedding(
    backend: EmbeddingBackend | None = None,
) -> BaseEmbedding:
    """
    설정 또는 인자로 임베딩 백엔드 선택.

    예)
    - settings.EMBEDDING_BACKEND = "openai"
    - create_embedding() → OpenAIEmbedding
    """
    backend = backend or getattr(settings, "EMBEDDING_BACKEND", "openai")

    if backend == "openai":
        return OpenAIEmbedding()
    # elif backend == "upstage":
    #     return UpstageEmbedding()
    # elif backend == "huggingface":
    #     return HuggingFaceEmbedding()
    else:
        raise ValueError(f"지원하지 않는 임베딩 백엔드: {backend}")
