# app/rag/schemas.py
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class FileSource:
    """원본 파일 정보"""
    path: Path
    source_type: str  # "local_file", "web", "s3", etc.
    mime_type: Optional[str] = None


@dataclass
class LoadedDocument:
    """로더에서 반환하는 문서 단위 (LangChain Document 래핑)"""
    page_content: str
    metadata: Dict[str, Any]
    source: FileSource
