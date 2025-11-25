# app/graphs/base/graph_registry.py
"""
그래프 레지스트리: 이름으로 그래프를 등록/조회/목록 조회.
Chain 레지스트리와 인터페이스를 통일.
"""
from __future__ import annotations

from typing import Dict, Type

from app.graphs.base.base_graph import BaseGraph

_GRAPH_REGISTRY: Dict[str, Type[BaseGraph]] = {}


def register_graph(name: str):
    """
    클래스 데코레이터:
    @register_graph("echo")
    class EchoGraph(BaseGraph): ...
    """

    def decorator(cls: Type[BaseGraph]) -> Type[BaseGraph]:
        if not issubclass(cls, BaseGraph):
            raise TypeError(
                f"register_graph('{name}') 대상 클래스는 BaseGraph를 상속해야 합니다. "
                f"(got: {cls.__name__})"
            )

        if name in _GRAPH_REGISTRY:
            existing = _GRAPH_REGISTRY[name].__name__
            raise ValueError(
                f"이미 이름이 '{name}'인 그래프가 등록되어 있습니다. (existing: {existing})"
            )

        _GRAPH_REGISTRY[name] = cls
        return cls

    return decorator


def register_graph_class(name: str, cls: Type[BaseGraph]) -> None:
    """
    데코레이터 대신 수동으로 그래프 클래스를 등록하고 싶을 때 사용.
    """
    if not issubclass(cls, BaseGraph):
        raise TypeError(
            f"register_graph_class('{name}') 대상 클래스는 BaseGraph를 상속해야 합니다. "
            f"(got: {cls.__name__})"
        )

    if name in _GRAPH_REGISTRY:
        existing = _GRAPH_REGISTRY[name].__name__
        raise ValueError(
            f"이미 이름이 '{name}'인 그래프가 등록되어 있습니다. (existing: {existing})"
        )

    _GRAPH_REGISTRY[name] = cls


def get_graph(name: str) -> Type[BaseGraph]:
    """
    이름으로 그래프 클래스를 조회.
    - 못 찾으면 KeyError 발생.
    """
    try:
        return _GRAPH_REGISTRY[name]
    except KeyError:
        raise KeyError(f"Graph '{name}' not found in registry")


def list_graphs() -> Dict[str, Type[BaseGraph]]:
    """
    등록된 그래프 목록 (복사본) 반환.
    - { "echo": EchoGraph, ... } 형태
    """
    return dict(_GRAPH_REGISTRY)
