from dataclasses import dataclass
from typing import List

from langchain_core.documents import Document

from app.rag.embeddings.factory import create_embedding
from app.rag.vectorstore.factory import create_vectorstore


@dataclass
class RagRetrieveConfig:
    persist_directory: str = "data/chroma"
    collection_name: str = "default"
    k: int = 5


def retrieve_docs(
    query: str,
    config: RagRetrieveConfig,
) -> List[Document]:
    embeddings = create_embedding()
    vs = create_vectorstore(
        embeddings=embeddings,
        persist_directory=config.persist_directory,
        collection_name=config.collection_name,
    )
    return vs.similarity_search(query, k=config.k)
