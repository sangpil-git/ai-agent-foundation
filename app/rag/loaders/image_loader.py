# app/rag/loaders/image_loader.py
"""
이미지 → 텍스트(캡션, OCR 등) 변환 로더.
"""
from pathlib import Path
from typing import List


def load_from_image(path: str | Path) -> List[str]:
    """
    이미지 파일을 받아 캡션/텍스트를 추출.
    현재는 placeholder.
    """
    # TODO: OCR, 비전 모델 연동
    return [f"[IMAGE:{Path(path).name}] (OCR/Caption not implemented)"]
