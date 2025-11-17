# app/chains/builtin/rag_qa_chain.py
"""
RAG 기반 Q&A 체인.

- 단일 질문(question)을 입력으로 받아
- RAG 파이프라인(simple_rag_answer)으로 답변을 생성한다.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from app.chains.base.base_chain import BaseChain
from app.chains.base.chain_registry import register_chain  # 현재 구조에 맞춰 유지
from app.rag.rag_pipeline import simple_rag_answer


@register_chain("rag_qa")
class RagQAChain(BaseChain):
    """
    question 하나 받아서 simple_rag_answer 로 처리하는 체인.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        *,
        top_k: int = 3,
    ) -> None:
        """
        Parameters
        ----------
        model_name : str | None
            나중에 LLM 선택 등에 사용할 수 있는 옵션.
            현재 simple_rag_answer 는 LLM 을 직접 사용하지 않으므로 보관만 한다.
        top_k : int
            RAG 검색 시 사용할 문서 개수.
            simple_rag_answer 의 top_k 로 그대로 전달된다.
        """
        self.model_name = model_name
        self.top_k = top_k

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # 1) question 유효성 검증
        raw_question: Any = input_data.get("question")
        if not isinstance(raw_question, str):
            raise ValueError("input_data['question'] 값은 문자열(str)이어야 합니다.")

        question = raw_question.strip()
        if not question:
            raise ValueError("질문(question)은 비어 있을 수 없습니다.")

        # 2) RAG 파이프라인 호출
        #    simple_rag_answer 는 현재 문자열을 반환
        answer = simple_rag_answer(question, top_k=self.top_k)

        # 3) 응답 구조 (나중에 meta/context 등 확장 가능)
        return {
            "question": question,
            "answer": answer,
        }
