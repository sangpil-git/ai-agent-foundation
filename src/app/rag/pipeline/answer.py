# app/rag/pipeline/answer.py
from __future__ import annotations

from typing import List

from langchain_core.documents import Document

from app.rag.pipeline.retrieval import retrieve_docs, RagRetrieveConfig
from app.core.llm import create_llm


def simple_rag_answer(
    question: str,
    *,
    top_k: int = 3,
    model_name: str | None = None,
) -> str:
    """
    RAG 최소 파이프라인:
    1) retrieve_docs() 로 문서 검색
    2) LLM 호출로 질문 + 문서 기반 답변 생성
    """

    # 1) 문서 검색 설정 구성
    config = RagRetrieveConfig(
        k=top_k,  # ✅ 최종 검색 개수를 여기서 세팅
        # 필요하면 persist_directory, collection_name도 외부에서 넘기도록 확장 가능
    )

    docs: List[Document] = retrieve_docs(
        query=question,
        config=config,  # ✅ top_k가 아니라 config로 전달
    )

    context_text = "\n\n".join(d.page_content for d in docs) if docs else ""

    llm = create_llm(model_name)

    prompt = (
        "다음은 질문에 답변하기 위한 문서입니다.\n\n"
        f"### Context ###\n{context_text}\n\n"
        f"### Question ###\n{question}\n\n"
        "문서를 참고하여 한국어로 자연스럽게 답변해 주세요:\n"
    )

    answer = llm.invoke(prompt)

    # 응답 타입 보정
    if hasattr(answer, "content"):
        return answer.content
    if isinstance(answer, dict):
        if "output_text" in answer:
            return answer["output_text"]
        if "text" in answer:
            return answer["text"]
    if isinstance(answer, str):
        return answer

    return str(answer)
