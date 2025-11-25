# app/rag/loaders/pdf_loader.py
from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader

from app.rag.loaders.base import BaseLoader
from app.resources.schema.rag_schemas import LoadedDocument


class PDFLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__(source_type="local_file", mime_type="application/pdf")

    def load(self, path: str | Path) -> List[LoadedDocument]:
        path = Path(path)
        self.log(f"Loading PDF: {path}")

        loader = PyPDFLoader(str(path))
        try:
            docs = loader.load()
        except Exception as e:
            self.log(f"Error loading PDF: {e}")
            raise

        source = self._make_source(path)
        results: List[LoadedDocument] = []

        for d in docs:
            meta = self._merge_metadata(
                base=d.metadata,
                extra={
                    "file_path": str(path),
                    "page": d.metadata.get("page"),
                },
            )
            results.append(
                LoadedDocument(
                    page_content=d.page_content,
                    metadata=meta,
                    source=source,
                )
            )
        return results


def load_pdf_file(path: str | Path) -> List[LoadedDocument]:
    return PDFLoader().load(path)
