# src/app/rag/embeddings/openai_embedding.py
from __future__ import annotations

from typing import List, Optional

from langchain_openai import OpenAIEmbeddings

from app.rag.embeddings.base import BaseEmbedding
from app.core.config.settings import settings


class OpenAIEmbedding(BaseEmbedding):
    """
    OpenAI 임베딩 백엔드 구현체.
    BaseEmbedding에서 제공하는 _prepare_text(s) 공통 로직을 그대로 사용.
    """

    def __init__(
        self,
        model: Optional[str] = None,
        *,
        max_text_length: int = 10_000,
        strip_whitespace: bool = True,
    ) -> None:
        # BaseEmbedding 공통 설정
        super().__init__(
            max_text_length=max_text_length,
            strip_whitespace=strip_whitespace,
        )

        self.model = model or settings.EMBEDDING_MODEL

        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

        try:
            self.client = OpenAIEmbeddings(
                model=self.model,
                api_key=settings.OPENAI_API_KEY,
            )
        except Exception as e:
            self.logger.error(f"[OpenAIEmbedding] 클라이언트 생성 오류: {e}")
            raise

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        processed = self._prepare_texts(texts)

        try:
            return self.client.embed_documents(processed)
        except Exception as e:
            self.logger.error(f"[OpenAIEmbedding] embed_documents 오류: {e}")
            raise RuntimeError(f"OpenAI embed_documents 실패: {e}") from e

    def embed_query(self, text: str) -> List[float]:
        processed = self._prepare_text(text)

        try:
            return self.client.embed_query(processed)
        except Exception as e:
            self.logger.error(f"[OpenAIEmbedding] embed_query 오류: {e}")
            raise RuntimeError(f"OpenAI embed_query 실패: {e}") from e
