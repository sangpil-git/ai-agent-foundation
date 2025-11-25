# app/rag/pipeline/indexing.py
from pathlib import Path
from typing import Iterable, List

from langchain_core.documents import Document

from app.rag.loaders.factory import load_any
from app.rag.splitter.text_splitter import (
    create_default_text_splitter,
    split_loaded_documents,
)
from app.rag.embeddings.factory import create_embedding  # Embeddings 리턴 버전이라고 가정
from app.rag.vectorstore.factory import create_vectorstore
from app.rag.pipeline.pipeline_config import RagIndexConfig


def build_index_from_files(
    file_paths: Iterable[str | Path],
    config: RagIndexConfig,
):
    loaded = []
    for path in file_paths:
        loaded.extend(load_any(path))

    splitter = create_default_text_splitter(
        # 필요하면 config.chunk_size 사용
    )
    chunks: List[Document] = split_loaded_documents(loaded, splitter=splitter)

    embeddings = create_embedding()  # 여기서는 LangChain Embeddings를 반환하는 버전 사용
    vs = create_vectorstore(
        embeddings=embeddings,
        persist_directory=config.persist_directory,
        collection_name=config.collection_name,
        documents=chunks,
    )
    vs.persist()
    return vs
