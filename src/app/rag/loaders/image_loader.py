# app/rag/loaders/image_loader.py
from __future__ import annotations

from pathlib import Path
from typing import List

from PIL import Image
import pytesseract

from app.rag.loaders.base import BaseLoader
from app.resources.schema.rag_schemas import LoadedDocument


class ImageOCRLoader(BaseLoader):
    def __init__(self, lang: str = "kor+eng") -> None:
        super().__init__(source_type="local_file", mime_type="image")
        self.lang = lang

    def load(self, path: str | Path) -> List[LoadedDocument]:
        path = Path(path)
        self.log(f"Loading image for OCR: {path}")

        try:
            image = Image.open(path)
            text = pytesseract.image_to_string(image, lang=self.lang)
        except Exception as e:
            self.log(f"Error in OCR: {e}")
            raise

        source = self._make_source(path)
        meta = {
            "file_path": str(path),
            "ocr_lang": self.lang,
        }

        return [
            LoadedDocument(
                page_content=text,
                metadata=meta,
                source=source,
            )
        ]


def load_image_ocr(path: str | Path, lang: str = "kor+eng") -> List[LoadedDocument]:
    return ImageOCRLoader(lang=lang).load(path)
