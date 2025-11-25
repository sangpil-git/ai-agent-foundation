# app/rag/vectorstore/chroma_store.py
from __future__ import annotations

from typing import List, Sequence, Optional

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma

from app.rag.vectorstore.base import BaseVectorStore


class ChromaVectorStore(BaseVectorStore):
    def __init__(
        self,
        embeddings: Embeddings,
        persist_directory: Optional[str] = None,
        collection_name: str = "default",
        documents: Optional[Sequence[Document]] = None,
    ) -> None:
        """
        :param embeddings: LangChain Embeddings 객체 (OpenAIEmbeddings 등)
        :param persist_directory: Chroma 디스크 경로
        :param collection_name: 컬렉션 이름
        :param documents: 초기 인덱싱할 문서들(optional)
        """
        if documents:
            self._store = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=persist_directory,
                collection_name=collection_name,
            )
        else:
            self._store = Chroma(
                embedding_function=embeddings,
                persist_directory=persist_directory,
                collection_name=collection_name,
            )

    def add_documents(self, docs: Sequence[Document]) -> None:
        if not docs:
            return
        self._store.add_documents(list(docs))

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        return self._store.similarity_search(query, k=k)

    def persist(self) -> None:
        try:
            self._store.persist()
        except Exception:
            # 메모리 모드 등에서는 persist가 의미 없을 수도 있으니 방어적으로 처리
            pass
