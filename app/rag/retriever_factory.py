# app/rag/retriever_factory.py
"""
VectorStore + Embeddings 를 이용한 Retriever 헬퍼.
"""
from typing import List

from app.rag.embeddings import embed_texts
from app.rag.vector_store import global_vector_store


def retrieve_relevant_docs(query: str, k: int = 3) -> List[str]:
    """
    쿼리 텍스트 기반으로 관련 문서 k개 반환.
    현재는 dummy 구현.
    """
    query_vec = embed_texts([query])[0]
    results = global_vector_store.similarity_search(query_vec, k=k)
    return [text for text, _score in results]
