# app/rag/loaders/file_loader.py
"""
파일(PDF, Word, 텍스트 등)을 읽어 문서로 변환하는 로더.
"""
from pathlib import Path
from typing import List


def load_from_file(path: str | Path) -> List[str]:
    """
    파일 경로를 받아 텍스트 문서 리스트로 변환.
    지금은 단순 텍스트 파일만 지원하는 예시.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    # TODO: PDF, Word, Markdown 등으로 확장
    text = p.read_text(encoding="utf-8", errors="ignore")
    return [text]
