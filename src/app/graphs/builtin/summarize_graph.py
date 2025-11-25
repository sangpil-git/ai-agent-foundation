# src/app/graphs/builtin/summarize_graph.py
from __future__ import annotations

from typing import Any, Dict, List

from langgraph.graph import StateGraph, START, END

from app.graphs.base.base_graph import BaseGraph
from app.graphs.base.graph_registry import register_graph
from app.graphs.base.graph_types import BaseGraphState
from app.chains.builtin.summarize_chain import SummarizeChain


class SummarizeState(BaseGraphState, total=False):
    """
    SummarizeGraph에서 사용하는 상태 정의.

    - text: 요약할 원문 텍스트
    - summary: 요약 결과
    - model: 사용한 모델명 (체인에서 반환하는 값)
    """
    text: str
    summary: str
    model: str


def summarize_node(state: SummarizeState) -> SummarizeState:
    """
    SummarizeChain을 호출해서 요약을 수행하는 노드.
    """
    text = state.get("text", "")
    model_name = state.get("model_name")  # 필요하면 state에 넣어 사용할 수도 있음

    # 기존 SummarizeChain 재사용
    chain = SummarizeChain(model_name=model_name)
    result = chain.invoke({"text": text})

    # SummarizeChain 결과 예:
    # { "model": "...", "output": "요약 텍스트 ..." }
    summary = result.get("output", "")
    model = result.get("model")

    return {
        **state,
        "summary": summary,
        "model": model,
    }


@register_graph("summarize")
class SummarizeGraph(BaseGraph):
    """
    요약용 Graph 기본 뼈대.

    - 입력: { "text": "요약할 텍스트...", (optional) "model_name": "gpt-4.1-mini" }
    - 출력: { "text": ..., "summary": ..., "model": ... }
    """

    def __init__(self) -> None:
        super().__init__(name="SummarizeGraph")

    # --------------------------
    # 1) 입력 검증
    # --------------------------
    def validate_input(self, input_data: Dict[str, Any]) -> None:
        raw_text = input_data.get("text")

        if raw_text is None:
            raise ValueError("'text' 필드는 반드시 필요합니다.")

        if not isinstance(raw_text, str):
            raise ValueError("'text' 값은 문자열(str)이어야 합니다.")

        if not raw_text.strip():
            raise ValueError("'text' 값은 비어 있을 수 없습니다.")

    # --------------------------
    # 2) 전처리
    # --------------------------
    def preprocess(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        - text 공백 정리
        - model_name 은 있으면 그대로 state에 포함
        """
        text = input_data.get("text", "")
        model_name = input_data.get("model_name")

        state: SummarizeState = {
            "text": text.strip(),
        }
        if model_name:
            # summarize_node 에서 사용할 수 있게 전달
            state["model_name"] = model_name  # BaseGraphState에 없는 필드도 동적 사용 가능

        return state

    # --------------------------
    # 3) 그래프 빌드
    # --------------------------
    def build(self):
        """
        StateGraph 구성:
        START -> summarize -> END
        """
        graph = StateGraph(SummarizeState)

        graph.add_node("summarize", summarize_node)

        graph.add_edge(START, "summarize")
        graph.add_edge("summarize", END)

        compiled = graph.compile()
        return compiled
