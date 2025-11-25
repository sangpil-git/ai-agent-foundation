# app/chains/builtin/rag_qa_chain.py

from __future__ import annotations

from typing import Any, Dict, Optional

from app.chains.base.base_chain import BaseChain, ChainInput, ChainOutput
from app.chains.base.chain_registry import register_chain
from app.rag.pipeline.answer import simple_rag_answer


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
        super().__init__(name="RagQAChain")
        self.model_name = model_name
        self.top_k = top_k

    def validate_input(self, input_data: ChainInput) -> None:
        raw_question: Any = input_data.get("question")

        if raw_question is None:
            raise ValueError("'question' 필드는 반드시 필요합니다.")
        if not isinstance(raw_question, str):
            raise ValueError("'question' 값은 문자열(str)이어야 합니다.")
        if not raw_question.strip():
            raise ValueError("질문('question')은 비어 있을 수 없습니다.")

    def preprocess(self, input_data: ChainInput) -> ChainInput:
        question = str(input_data.get("question", "")).strip()
        return {**input_data, "question": question}

    def run(self, data: ChainInput) -> ChainOutput:
        question: str = data["question"]

        # simple_rag_answer 가 나중에 dict 를 반환해도 대응 가능하도록 설계
        rag_result = simple_rag_answer(question, top_k=self.top_k, model_name=self.model_name)

        if isinstance(rag_result, dict):
            answer = rag_result.get("answer", "")
            context_docs = rag_result.get("context_docs", [])
        else:
            answer = str(rag_result)
            context_docs = []

        return {
            "question": question,
            "answer": answer,
            "context_docs": context_docs,
        }

    def postprocess(self, result: ChainOutput) -> ChainOutput:
        result.setdefault("question", "")
        result.setdefault("answer", "")
        result.setdefault("context_docs", [])
        return result
