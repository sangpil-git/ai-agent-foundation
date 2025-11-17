# app/tools/rag_tools.py
from typing import List
from app.tools.base import registered_tool
from app.rag.retriever_factory import retrieve_relevant_docs


@registered_tool("rag_search")
def rag_search_tool(query: str, k: int = 3) -> List[str]:
    """
    질의(query)를 기반으로 관련 문서 k개를 반환하는 RAG 검색 툴.
    """
    return retrieve_relevant_docs(query, k=k)
