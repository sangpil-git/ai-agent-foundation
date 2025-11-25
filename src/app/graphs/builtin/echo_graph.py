# src/app/graphs/builtin/echo_graph.py
from __future__ import annotations

from typing import Any, Dict, TypedDict

from langgraph.graph import StateGraph, START, END

from app.graphs.base.base_graph import BaseGraph
from app.graphs.base.graph_registry import register_graph


# 1) State 정의 (TypedDict 사용)
class EchoState(TypedDict, total=False):
    """
    아주 단순한 state 정의.
    - 입력: text
    - 출력: result
    """
    text: str
    result: str


# 2) 노드 함수 정의
def echo_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    입력으로 받은 text를 그대로 result에 넣어주는 노드.
    """
    text = state.get("text", "")
    return {
        **state,
        "result": f"echo: {text}",
    }


# 3) 그래프 클래스
@register_graph("echo")
class EchoGraph(BaseGraph):
    """
    가장 간단한 예제 그래프.
    - 입력: { "text": "hello" }
    - 출력: { "text": "hello", "result": "echo: hello" }
    """

    def __init__(self) -> None:
        # 이름만 명시적으로 넣어줌 (로그/디버깅용)
        super().__init__(name="EchoGraph")

    # BaseGraph 패턴에 맞춰 필요한 훅만 선택적으로 override

    def validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        필수 입력값 검증.
        """
        if "text" not in input_data:
            raise ValueError("'text' 필드는 반드시 필요합니다.")

    def preprocess(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        전처리: text를 string으로 강제 캐스팅 정도만 수행.
        """
        text = str(input_data.get("text", ""))
        return {
            **input_data,
            "text": text,
        }

    def build(self):
        """
        StateGraph를 생성하고 compile()한 결과를 반환.
        BaseGraph.compiled에서 lazy로 한 번만 호출됨.
        """
        graph = StateGraph(EchoState)

        # 노드 등록
        graph.add_node("echo", echo_node)

        # 엣지 정의
        graph.add_edge(START, "echo")
        graph.add_edge("echo", END)

        compiled = graph.compile()
        return compiled
