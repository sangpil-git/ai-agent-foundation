# app/rag/loaders/factory.py
from pathlib import Path
from typing import List, Callable, Dict

from app.resources.schema.rag_schemas import LoadedDocument
from app.rag.loaders.text_loader import load_text_file
from app.rag.loaders.pdf_loader import load_pdf_file
from app.rag.loaders.excel_loader import load_csv_file
from app.rag.loaders.image_loader import load_image_ocr


LoaderFunc = Callable[[str | Path], List[LoadedDocument]]

EXTENSION_MAP: Dict[str, LoaderFunc] = {
    ".txt": load_text_file,
    ".md": load_text_file,
    ".csv": load_csv_file,
    ".pdf": load_pdf_file,
    ".png": load_image_ocr,
    ".jpg": load_image_ocr,
    ".jpeg": load_image_ocr,
}


def load_any(path: str | Path) -> List[LoadedDocument]:
    p = Path(path)
    ext = p.suffix.lower()
    if ext not in EXTENSION_MAP:
        raise ValueError(f"지원하지 않는 파일 확장자입니다: {ext}")
    return EXTENSION_MAP[ext](p)
