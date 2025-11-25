# app/rag/splitter/text_splitter.py
from typing import List, Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.resources.schema.rag_schemas import LoadedDocument
from app.rag.splitter.splitter_config import TextSplitterConfig


def create_default_text_splitter(
    config: Optional[TextSplitterConfig] = None,
) -> RecursiveCharacterTextSplitter:
    config = config or TextSplitterConfig()
    return RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )


def split_loaded_documents(
    loaded_docs: List[LoadedDocument],
    splitter: Optional[RecursiveCharacterTextSplitter] = None,
) -> List[Document]:
    if splitter is None:
        splitter = create_default_text_splitter()

    lc_docs = [
        Document(
            page_content=d.page_content,
            metadata={
                **d.metadata,
                "source_type": d.source.source_type,
                "file_path": str(d.source.path) if d.source.path else None,
                "mime_type": d.source.mime_type,
            },
        )
        for d in loaded_docs
    ]
    return splitter.split_documents(lc_docs)
