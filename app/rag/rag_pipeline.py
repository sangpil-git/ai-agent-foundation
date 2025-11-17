# app/rag/rag_pipeline.py
"""
RAG end-to-end 파이프라인 예시.

- 질문(question)을 입력으로 받아
- retriever 에서 관련 문서를 조회하고(context)
- 현재는 context 를 그대로 answer 형식에 붙여서 반환
- 나중에 LLM 호출 + 프롬프트 구성으로 확장 예정
"""

from typing import List

from app.rag.retriever_factory import retrieve_relevant_docs


def simple_rag_answer(question: str, *, top_k: int = 3) -> str:
    """
    매우 단순한 RAG 답변 예시.

    Parameters
    ----------
    question : str
        사용자 질문 텍스트.
    top_k : int, optional
        retriever 에서 가져올 문서 개수 (기본값: 3)

    Returns
    -------
    str
        포맷팅된 문자열 형태의 RAG 답변.
        (Q + 컨텍스트를 단순히 이어붙인 형태)
    """
    question = question.strip()
    if not question:
        raise ValueError("question 값은 비어 있을 수 없습니다.")

    # 1) 관련 문서 검색
    docs: List[str] = retrieve_relevant_docs(question, k=top_k)

    # 2) 컨텍스트 문자열 생성
    if docs:
        # 문서 여러 개를 구분선으로 연결
        context = "\n---\n".join(docs)
    else:
        context = "(no context)"

    # 3) 현재는 LLM 없이 단순 포맷팅된 문자열을 반환
    #    나중에 여기서 LLM 호출 로직으로 확장하면 된다.
    formatted_answer = (
        "[RAG-ANSWER]\n"
        f"Q: {question}\n\n"
        "CTX:\n"
        f"{context}"
    )

    return formatted_answer

    # 예시: LLM 연동 시 (나중에)
    # from app.core.llm import get_default_llm
    # llm = get_default_llm()
    # prompt = build_rag_prompt(question=question, context=context)
    # llm_answer = llm.invoke(prompt)
    # return llm_answer
