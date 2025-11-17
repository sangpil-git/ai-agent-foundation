"""
Tools package for Agent Framework.

Auto-imports every module inside this package so that
all @registered_tool decorators execute and tools are registered.
"""

import pkgutil
import importlib
from pathlib import Path

from app.core.llm import tool_registry
from .base import registered_tool

# Auto-discover and import all modules in this folder
_package_dir = Path(__file__).resolve().parent

for module in pkgutil.iter_modules([str(_package_dir)]):
    if module.name not in ["base", "__init__"]:
        importlib.import_module(f"{__name__}.{module.name}")


__all__ = [
    "registered_tool",
    "tool_registry",
]
