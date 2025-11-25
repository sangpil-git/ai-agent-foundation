# app/rag/loaders/excel_loader.py
from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_community.document_loaders import CSVLoader

from app.rag.loaders.base import BaseLoader
from app.resources.schema.rag_schemas import LoadedDocument


class CSVFileLoader(BaseLoader):
    def __init__(self, encoding: str = "utf-8") -> None:
        super().__init__(source_type="local_file", mime_type="text/csv")
        self.encoding = encoding

    def load(self, path: str | Path) -> List[LoadedDocument]:
        path = Path(path)
        self.log(f"Loading CSV: {path}")

        loader = CSVLoader(str(path), encoding=self.encoding)
        try:
            docs = loader.load()
        except Exception as e:
            self.log(f"Error loading CSV: {e}")
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


def load_csv_file(path: str | Path, encoding: str = "utf-8") -> List[LoadedDocument]:
    return CSVFileLoader(encoding=encoding).load(path)
