# app/graphs/__init__.py
"""
graphs 패키지 초기화.

- base.graph_registry 의 get_graph / register_graph export
- builtin 하위 그래프들을 자동 import → @register_graph 데코레이터 실행
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from app.graphs.base.graph_registry import get_graph, register_graph, list_graphs

__all__ = ["get_graph", "register_graph", "list_graphs"]


def _auto_import_builtin_graphs() -> None:
    """app/graphs/builtin 폴더의 모든 모듈 자동 import."""
    package_dir = Path(__file__).resolve().parent / "builtin"
    package_name = f"{__name__}.builtin"

    if not package_dir.exists():
        return

    for module in pkgutil.iter_modules([str(package_dir)]):
        importlib.import_module(f"{package_name}.{module.name}")


_auto_import_builtin_graphs()
