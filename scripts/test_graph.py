# scripts/test_graph.py
"""
개별 그래프 로컬 테스트용 스크립트.
"""
from app.graphs.base.graph_registry import get_graph


def main():
    GraphCls = get_graph("support_bot")
    graph = GraphCls()
    result = graph.run({"question": "테스트 질문"})
    print(result)


if __name__ == "__main__":
    main()
