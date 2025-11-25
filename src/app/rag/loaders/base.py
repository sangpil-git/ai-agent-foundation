# src/app/rag/loaders/base.py
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.resources.schema.rag_schemas import FileSource, LoadedDocument


class BaseLoader(ABC):
    """
    모든 로더들의 공통 기반 클래스.
    - 공통 로깅
    - 공통 예외 처리
    - 공통 메타데이터 생성
    - FileSource 생성
    """

    def __init__(
        self,
        source_type: str,
        mime_type: Optional[str] = None,
        enable_logging: bool = True,
    ) -> None:
        self.source_type = source_type
        self.mime_type = mime_type
        self.enable_logging = enable_logging
        self.logger = logging.getLogger(self.__class__.__name__)

    # ----------------------------------------------------------------------
    # 공통 로깅
    # ----------------------------------------------------------------------
    def log(self, message: str):
        if self.enable_logging:
            self.logger.info(f"[{self.__class__.__name__}] {message}")

    # ----------------------------------------------------------------------
    # 파일/URL 공통 처리
    # ----------------------------------------------------------------------
    def _make_source(self, path: str | Path | None) -> FileSource:
        """
        모든 로더가 공통으로 사용하는 FileSource 생성기
        - path가 있을 수도, 없을 수도 있음(API/Web 등)
        """
        return FileSource(
            path=Path(path) if path else None,
            source_type=self.source_type,
            mime_type=self.mime_type,
        )

    # ----------------------------------------------------------------------
    # 메타데이터 공통 정제
    # ----------------------------------------------------------------------
    def _merge_metadata(
        self, base: Dict[str, Any], extra: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        merged = {**base}
        if extra:
            merged.update(extra)
        return merged

    # ----------------------------------------------------------------------
    # 하위 클래스 의무 구현
    # ----------------------------------------------------------------------
    @abstractmethod
    def load(self, *args, **kwargs) -> List[LoadedDocument]:
        """
        모든 하위 클래스는 load() 하나만 구현하면 됨.
        """
        raise NotImplementedError
