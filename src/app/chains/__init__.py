# app/chains/__init__.py
"""
chains 패키지 초기화.

- base.chain_registry 의 get_chain / register_chain 을 export
- builtin 하위 체인들을 자동 import → @register_chain 자동 등록
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from app.chains.base.chain_registry import get_chain, register_chain

__all__ = ["get_chain", "register_chain"]


def _auto_import_builtin_chains() -> None:
    """app/chains/builtin 폴더의 모든 모듈 자동 import."""
    package_dir = Path(__file__).resolve().parent / "builtin"
    package_name = f"{__name__}.builtin"

    if not package_dir.exists():
        return

    for module in pkgutil.iter_modules([str(package_dir)]):
        importlib.import_module(f"{package_name}.{module.name}")


_auto_import_builtin_chains()
