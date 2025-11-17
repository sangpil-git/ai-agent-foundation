# tests/test_graphs.py
from app.graphs.base.graph_registry import get_graph


def test_support_bot_graph_basic():
    GraphCls = get_graph("support_bot")
    graph = GraphCls()
    result = graph.run({"question": "hello"})
    assert "answer" in result
