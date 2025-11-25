# app/tools/__init__.py
"""
Tools package for Agent Framework.

- Auto-imports all modules inside 'tools' and 'tools/builtin'
  so @registered_tool decorators run and tools are registered.

Usage:
    from app.tools import tool_registry, registered_tool
"""

from __future__ import annotations

import pkgutil
import importlib
from pathlib import Path

from .tool_registry import tool_registry
from .base import registered_tool


def _auto_import_modules(package_path: Path, base_package: str) -> None:
    """
    지정한 폴더 안의 모든 .py 모듈을 자동으로 import.
    base_package: 예) "app.tools" 또는 "app.tools.builtin"
    """
    for module in pkgutil.iter_modules([str(package_path)]):
        name = module.name

        # 내부에서 직접 import 하는 모듈들은 제외
        if name in {"__init__", "base", "tool_registry"}:
            continue
        if name.startswith("_"):
            continue

        importlib.import_module(f"{base_package}.{name}")


# 현재 tools 패키지 디렉토리
_tools_dir = Path(__file__).resolve().parent

# 1) tools/ 내부 모듈 자동 로딩 (예: builtin 패키지 포함)
_auto_import_modules(_tools_dir, __name__)  # __name__ == "app.tools"

# 2) tools/builtin/ 내부 모듈 자동 로딩
_builtin_dir = _tools_dir / "builtin"
if _builtin_dir.exists():
    _auto_import_modules(_builtin_dir, f"{__name__}.builtin")  # "app.tools.builtin"


__all__ = [
    "registered_tool",
    "tool_registry",
]
