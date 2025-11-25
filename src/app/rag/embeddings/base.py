# src/app/rag/embeddings/base.py
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import List


class BaseEmbedding(ABC):
    """
    모든 임베딩 백엔드 공통 베이스 클래스.
    - 길이 제한, 공백 제거, 로깅 등 공통 유틸을 여기서 처리
    """

    def __init__(
        self,
        *,
        max_text_length: int = 10_000,
        strip_whitespace: bool = True,
    ) -> None:
        """
        :param max_text_length: 너무 긴 텍스트를 임베딩 전에 잘라낼 최대 길이
        :param strip_whitespace: 앞뒤 공백 제거 여부
        """
        self.max_text_length = max_text_length
        self.strip_whitespace = strip_whitespace
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------
    # 공통 유틸
    # ------------------------------
    def _prepare_text(self, text: str) -> str:
        """텍스트 정제 (공백 제거 + 길이 제한). 모든 하위 클래스에서 재사용."""
        if self.strip_whitespace:
            text = text.strip()

        if len(text) > self.max_text_length:
            self.logger.warning(
                f"[{self.__class__.__name__}] 입력 길이 {len(text)} > "
                f"max_text_length({self.max_text_length}) → 자동 truncate"
            )
            text = text[: self.max_text_length]

        return text

    def _prepare_texts(self, texts: List[str]) -> List[str]:
        """여러 개 텍스트를 한 번에 정제."""
        return [self._prepare_text(t) for t in texts]

    # ------------------------------
    # 인터페이스
    # ------------------------------
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        여러 문서(문단)를 임베딩.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """
        검색 쿼리 한 개를 임베딩.
        """
        raise NotImplementedError
