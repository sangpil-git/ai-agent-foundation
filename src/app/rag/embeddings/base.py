# src/app/rag/embeddings/base.py
from abc import ABC, abstractmethod
from typing import List


class BaseEmbedding(ABC):
    """
    RAG에서 사용할 공통 Embedding 인터페이스.
    Provider(OpenAI, Upstage 등)에 상관없이 이 인터페이스만 바라보고 사용.
    """

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """여러 문장을 임베딩."""
        raise NotImplementedError

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """검색용 쿼리 임베딩."""
        raise NotImplementedError
