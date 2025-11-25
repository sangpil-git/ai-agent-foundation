# app/chains/chain_registry.py
"""
체인 레지스트리: 이름으로 체인을 등록/조회/목록 조회.
Graph 레지스트리와 인터페이스를 통일.
"""
from __future__ import annotations

from typing import Dict, Type

from app.chains.base.base_chain import BaseChain

_CHAIN_REGISTRY: Dict[str, Type[BaseChain]] = {}


def register_chain(name: str):
    """
    클래스 데코레이터:
    @register_chain("echo")
    class EchoChain(BaseChain): ...
    """

    def decorator(cls: Type[BaseChain]) -> Type[BaseChain]:
        # BaseChain 상속 여부 체크
        if not issubclass(cls, BaseChain):
            raise TypeError(
                f"register_chain('{name}') 대상 클래스는 BaseChain을 상속해야 합니다. "
                f"(got: {cls.__name__})"
            )

        # 중복 등록 방지
        if name in _CHAIN_REGISTRY:
            existing = _CHAIN_REGISTRY[name].__name__
            raise ValueError(
                f"이미 이름이 '{name}'인 체인이 등록되어 있습니다. (existing: {existing})"
            )

        _CHAIN_REGISTRY[name] = cls
        return cls

    return decorator


def register_chain_class(name: str, cls: Type[BaseChain]) -> None:
    """
    데코레이터 대신 수동으로 체인 클래스를 등록하고 싶을 때 사용.
    """
    if not issubclass(cls, BaseChain):
        raise TypeError(
            f"register_chain_class('{name}') 대상 클래스는 BaseChain을 상속해야 합니다. "
            f"(got: {cls.__name__})"
        )

    if name in _CHAIN_REGISTRY:
        existing = _CHAIN_REGISTRY[name].__name__
        raise ValueError(
            f"이미 이름이 '{name}'인 체인이 등록되어 있습니다. (existing: {existing})"
        )

    _CHAIN_REGISTRY[name] = cls


def get_chain(name: str) -> Type[BaseChain]:
    """
    이름으로 체인 클래스를 조회.
    - 못 찾으면 KeyError 발생.
    """
    try:
        return _CHAIN_REGISTRY[name]
    except KeyError:
        raise KeyError(f"Chain '{name}' not found in registry")


def list_chains() -> Dict[str, Type[BaseChain]]:
    """
    등록된 체인 목록 (복사본) 반환.
    - { "echo": EchoChain, ... } 형태
    """
    return dict(_CHAIN_REGISTRY)
