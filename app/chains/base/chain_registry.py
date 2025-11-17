# app/chains/chain_registry.py
"""
체인 레지스트리: 이름으로 체인을 등록/조회할 수 있도록 관리.
"""
from typing import Dict, Type

from app.chains.base.base_chain import BaseChain

_CHAIN_REGISTRY: Dict[str, Type[BaseChain]] = {}


def register_chain(name: str):
    """
    클래스 데코레이터:
    @register_chain("echo")
    class EchoChain(BaseChain): ...
    """
    def decorator(cls: Type[BaseChain]):
        _CHAIN_REGISTRY[name] = cls
        return cls
    return decorator


def get_chain(name: str) -> Type[BaseChain]:
    if name not in _CHAIN_REGISTRY:
        raise KeyError(f"Chain '{name}' not found")
    return _CHAIN_REGISTRY[name]


def list_chains() -> Dict[str, Type[BaseChain]]:
    return dict(_CHAIN_REGISTRY)
