from typing import List
from functools import lru_cache

from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from core.config import settings


# RAG VectorStore 초기화
@lru_cache
def get_vectorstore() -> Chroma:
    """
    Lazy 초기화:
    - import 시점에는 Embeddings/VectorStore를 만들지 않는다.
    - 실제로 RAG 검색이 필요할 때 최초 1번만 생성한다.
    - .env -> settings.OPENAI_API_KEY 값을 api_key로 직접 주입한다.
    """
    embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
    return Chroma(
        collection_name="agent-foundation",
        embedding_function=embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIR,
    )


def index_documents(docs: List[Document]) -> None:
    """
    배치/CLI에서 문서들을 인덱싱할 때 사용.
    """
    vs = get_vectorstore()
    vs.add_documents(docs)
    vs.persist()


@tool("db_knowledge_search")
def db_knowledge_search(query: str, k: int = 5) -> str:
    """
    RAG 검색 Tool:
    - query로 유사도 검색을 수행하고
    - 간단한 텍스트 형태로 반환.
    """
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=k)

    snippets = []
    for d in docs:
        meta = d.metadata or {}
        source_type = meta.get("source_type", "text")
        source = meta.get("source", "unknown")
        snippets.append(f"[{source_type}] {source}\n{d.page_content[:300]}")

    return "\n\n---\n\n".join(snippets)


# 예시: 이미지/문서/API json 처리용 helper
def make_doc_from_text(
    content: str, source: str, source_type: str = "text"
) -> Document:
    return Document(
        page_content=content, metadata={"source": source, "source_type": source_type}
    )
