# app/core/__init__.py
"""
핵심 설정, 레지스트리, LLM 팩토리 모듈 패키지.

다른 레이어에서 아래처럼 간단히 쓸 수 있도록 re-export:
    from app.core import settings, get_logger, create_llm, ...
"""

from __future__ import annotations

from .config.settings import settings
from .config.loader import load_yaml
from .logging import setup_logging
from .logging.logger import get_logger
from .llm import create_llm, model_registry, prompt_registry
from .tracing import init_langsmith

__all__ = [
    "settings",
    "load_yaml",
    "setup_logging",
    "get_logger",
    "create_llm",
    "model_registry",
    "prompt_registry",
    "init_langsmith",
]
