# app/rag/vectorstore/factory.py
from __future__ import annotations

from typing import Literal, Optional, Sequence

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from app.rag.vectorstore.base import BaseVectorStore
from app.rag.vectorstore.chroma_store import ChromaVectorStore
from app.core.config.settings import settings

VectorStoreBackend = Literal["chroma"]  # 나중에 "qdrant", "pgvector" 추가


def create_vectorstore(
    backend: Optional[VectorStoreBackend] = None,
    embeddings: Optional[Embeddings] = None,
    persist_directory: Optional[str] = None,
    collection_name: str = "default",
    documents: Optional[Sequence[Document]] = None,
) -> BaseVectorStore:
    backend = backend or getattr(settings, "VECTORSTORE_BACKEND", "chroma")

    if backend == "chroma":
        if embeddings is None:
            raise ValueError("ChromaVectorStore 생성 시 embeddings는 필수입니다.")
        return ChromaVectorStore(
            embeddings=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name,
            documents=documents,
        )

    raise ValueError(f"지원하지 않는 벡터스토어 백엔드: {backend}")
