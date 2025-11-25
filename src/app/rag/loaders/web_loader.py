# app/rag/loaders/web_loader.py
from __future__ import annotations

from typing import List

from langchain_community.document_loaders import WebBaseLoader

from app.rag.loaders.base import BaseLoader
from app.resources.schema.rag_schemas import LoadedDocument


class WebPageLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__(source_type="web", mime_type="text/html")

    def load(self, url: str) -> List[LoadedDocument]:
        self.log(f"Loading web page: {url}")

        loader = WebBaseLoader([url])
        try:
            docs = loader.load()
        except Exception as e:
            self.log(f"Error loading web page: {e}")
            raise

        source = self._make_source(None)
        results: List[LoadedDocument] = []

        for d in docs:
            meta = self._merge_metadata(
                base=d.metadata,
                extra={"url": url},
            )
            results.append(
                LoadedDocument(
                    page_content=d.page_content,
                    metadata=meta,
                    source=source,
                )
            )
        return results


def load_web_page(url: str) -> List[LoadedDocument]:
    return WebPageLoader().load(url)
