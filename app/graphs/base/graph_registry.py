# app/graphs/base/graph_registry.py
"""
Graph 레지스트리.

- 이름으로 Graph 클래스를 등록/조회할 수 있도록 관리.
"""

from typing import Dict, Type

from app.graphs.base.base_graph import BaseGraph

_GRAPH_REGISTRY: Dict[str, Type[BaseGraph]] = {}


def register_graph(name: str):
    """
    클래스 데코레이터:
    @register_graph("support_bot")
    class SupportBotGraph(BaseGraph): ...
    """
    def decorator(cls: Type[BaseGraph]):
        _GRAPH_REGISTRY[name] = cls
        return cls

    return decorator


def get_graph(name: str) -> Type[BaseGraph]:
    try:
        return _GRAPH_REGISTRY[name]
    except KeyError:
        raise KeyError(f"Graph '{name}' not found. 등록된 그래프 이름을 확인하세요.")


def list_graphs() -> Dict[str, Type[BaseGraph]]:
    return dict(_GRAPH_REGISTRY)
