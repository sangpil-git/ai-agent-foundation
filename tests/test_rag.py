# tests/test_rag.py
from src.app.rag.rag_pipeline import simple_rag_answer


def test_simple_rag_answer():
    res = simple_rag_answer("테스트")
    assert "RAG-ANSWER" in res
