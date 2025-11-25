# app/chains/__init__.py
"""
Chains package.

- builtin 체인들을 자동 import 해서
  @register_chain 데코레이터가 실행되도록 한다.
"""

from __future__ import annotations

import pkgutil
import importlib
from pathlib import Path


def _auto_import_modules(package_path: Path, base_package: str) -> None:
    for module in pkgutil.iter_modules([str(package_path)]):
        name = module.name
        if name.startswith("_"):
            continue
        importlib.import_module(f"{base_package}.{name}")


_chains_dir = Path(__file__).resolve().parent
_builtin_dir = _chains_dir / "builtin"

if _builtin_dir.exists():
    _auto_import_modules(_builtin_dir, "app.chains.builtin")

