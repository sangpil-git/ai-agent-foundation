# app/rag/vector_store.py
"""
벡터 스토어 추상화.
실제 구현은 Chroma, pgvector, FAISS 등으로 교체 가능.
"""
from typing import List, Tuple


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._texts: List[str] = []
        self._vectors: List[list[float]] = []

    def add(self, texts: List[str], vectors: List[list[float]]) -> None:
        self._texts.extend(texts)
        self._vectors.extend(vectors)

    def similarity_search(self, query_vector: list[float], k: int = 3) -> List[Tuple[str, float]]:
        """
        매우 단순한 dummy similarity 계산 (실제는 코사인 유사도 등).
        """
        # TODO: 실제 유사도 계산 구현
        return [(t, 0.0) for t in self._texts[:k]]


# 간단한 싱글톤 예시
global_vector_store = InMemoryVectorStore()
