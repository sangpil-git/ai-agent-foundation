# src/app/graphs/builtin/rag_qa_graph.py
from __future__ import annotations

from typing import Dict, Any, List

from langgraph.graph import StateGraph, START, END
from langchain_core.documents import Document

from app.graphs.base.base_graph import BaseGraph
from app.graphs.base.graph_registry import register_graph
from app.graphs.base.graph_types import BaseGraphState

# 나중에 실제 구현 시:
# from app.rag.pipeline.retrieval import retrieve_docs
# from app.core.llm import create_llm


class RagState(BaseGraphState, total=False):
    """
    RAG 그래프용 state 예시.

    기본 필드:
    - question: 사용자 질문
    - answer: 최종 답변
    - context_docs: 검색된 문서 리스트
    """
    question: str
    answer: str
    context_docs: List[Document]


def retrieve_node(state: RagState) -> RagState:
    """
    질문 → 관련 문서 검색.
    TODO: 실제 retrieve_docs 호출로 구현.
    """
    question = state.get("question", "")

    # TODO: 실제 RAG 파이프라인 연결 예시
    # cfg = RagRetrieveConfig(...)
    # docs = retrieve_docs(question, cfg)
    docs: List[Document] = []

    return {
        **state,
        "context_docs": docs,
    }


def answer_node(state: RagState) -> RagState:
    """
    LLM을 사용해 최종 답변 생성.
    TODO: create_llm(...) + 프롬프트 템플릿 연결.
    """
    question = state.get("question", "")
    docs = state.get("context_docs", [])

    # TODO: 예시
    # llm = create_llm(model_name="gpt-4.1-mini")
    # context_text = "\n\n".join(d.page_content for d in docs)
    # prompt = f"Question: {question}\n\nContext:\n{context_text}\n\nAnswer in Korean:"
    # answer = llm.invoke(prompt)

    answer = f"(stub) '{question}'에 대한 RAG 답변"

    return {
        **state,
        "answer": answer,
    }


@register_graph("rag_qa")
class RagQAGraph(BaseGraph):
    """
    RAG QA용 기본 골격 그래프.
    - START -> retrieve -> answer -> END

    입력 예:
    {
      "question": "사내 휴가 규정 요약해줘"
    }

    출력 예 (stub):
    {
      "question": "...",
      "context_docs": [...],
      "answer": "(stub) '...'에 대한 RAG 답변"
    }
    """

    def __init__(self) -> None:
        super().__init__(name="RagQAGraph")

    # --------------------------
    # BaseGraph 공통 훅 override
    # --------------------------
    def validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        필수 입력값 검증.
        """
        if "question" not in input_data:
            raise ValueError("'question' 필드는 반드시 필요합니다.")

    def preprocess(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        전처리: question을 문자열로 강제 캐스팅해서 넣어줌.
        추후 여기서 session_id, user_id 등 공통 메타도 추가 가능.
        """
        question = str(input_data.get("question", "")).strip()
        return {
            **input_data,
            "question": question,
        }

    def postprocess(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        후처리: 최소한 answer가 없을 때 기본 메시지 정도만 보정.
        """
        if "answer" not in result:
            result["answer"] = "(no answer generated)"
        return result

    # --------------------------
    # 그래프 빌드
    # --------------------------
    def build(self):
        """
        StateGraph를 생성하고 compile()한 결과를 반환.
        BaseGraph.compiled에서 lazy로 한 번만 호출됨.
        """
        graph = StateGraph(RagState)

        # 노드 등록
        graph.add_node("retrieve", retrieve_node)
        graph.add_node("answer", answer_node)

        # 엣지 정의
        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "answer")
        graph.add_edge("answer", END)

        compiled = graph.compile()
        return compiled
