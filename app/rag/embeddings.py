# app/rag/embeddings.py
"""
임베딩 생성 헬퍼.
향후 OpenAI, HuggingFace 임베딩 모델 교체를 여기서 처리.
"""
from typing import List


def embed_texts(texts: List[str]) -> List[list[float]]:
    """
    텍스트 리스트 → 벡터 리스트로 변환.
    현재는 dummy 값 반환.
    """
    # TODO: OpenAI Embeddings, sentence-transformers 등 연동
    return [[0.0] * 10 for _ in texts]
