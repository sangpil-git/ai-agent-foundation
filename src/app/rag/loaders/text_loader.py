# app/rag/loaders/text_loader.py
from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_community.document_loaders import TextLoader

from app.rag.loaders.base import BaseLoader
from app.resources.schema.rag_schemas import LoadedDocument


class TextFileLoader(BaseLoader):
    def __init__(self, encoding: str = "utf-8") -> None:
        super().__init__(source_type="local_file", mime_type="text/plain")
        self.encoding = encoding

    def load(self, path: str | Path) -> List[LoadedDocument]:
        path = Path(path)
        self.log(f"Loading text file: {path}")

        try:
            docs = TextLoader(str(path), encoding=self.encoding).load()
        except Exception as e:
            self.log(f"Error loading text file: {e}")
            raise

        source = self._make_source(path)

        results: List[LoadedDocument] = []
        for d in docs:
            meta = self._merge_metadata(
                base=d.metadata,
                extra={"file_path": str(path)},
            )

            results.append(
                LoadedDocument(
                    page_content=d.page_content,
                    metadata=meta,
                    source=source,
                )
            )
        return results


# 기존 코드와 호환용 함수
def load_text_file(path: str | Path, encoding: str = "utf-8") -> List[LoadedDocument]:
    return TextFileLoader(encoding=encoding).load(path)
