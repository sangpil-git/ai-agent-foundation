# app/rag/vectorstore/base.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Sequence

from langchain_core.documents import Document


class BaseVectorStore(ABC):
    """
    다양한 벡터스토어(Chroma, Qdrant, PGVector 등)를
    동일한 인터페이스로 다루기 위한 얇은 추상화.
    """

    @abstractmethod
    def add_documents(self, docs: Sequence[Document]) -> None:
        """문서 추가 (인덱싱 시 사용)"""
        raise NotImplementedError

    @abstractmethod
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """RAG 검색 시 사용"""
        raise NotImplementedError

    def persist(self) -> None:
        """
        영속화가 필요한 백엔드(Chroma 등)는 override,
        메모리 기반이면 pass.
        """
        return None
