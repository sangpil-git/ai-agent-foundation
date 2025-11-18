# app/graphs/support_bot_graph.py
"""
예시: RAG 기반 Q&A 지원 봇 그래프.
"""
from typing import Any, Dict

from app.graphs.base.base_graph import BaseGraph
from app.graphs.base.graph_registry import register_graph
from app.core.llm import create_llm
from app.rag.rag_pipeline import simple_rag_answer


@register_graph("support_bot")
class SupportBotGraph(BaseGraph):
    """
    단순 RAG Q&A용 예시 그래프.
    """

    def __init__(self, model_name: str | None = None):
        self.llm = create_llm(model_name)

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        question = input_data.get("question", "")
        # TODO: 실제로는 self.llm 과 RAG 파이프라인을 연결
        answer = simple_rag_answer(question)
        return {
            "question": question,
            "answer": answer,
        }
