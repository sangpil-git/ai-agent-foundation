# app/tools/builtin/rag_tools.py
from app.tools.base import registered_tool
from app.rag.pipeline.answer import simple_rag_answer


@registered_tool("rag_query")
def rag_query(question: str, top_k: int = 3, model_name: str | None = None) -> str:
    """
    RAG 파이프라인 기반 질문 답변 Tool.
    """
    return simple_rag_answer(
        question=question,
        top_k=top_k,
        model_name=model_name,
    )
