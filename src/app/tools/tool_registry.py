# app/tools/tool_registry.py
"""
tools.yml 에 정의된 툴들을 코드 상의 함수/객체와 매핑하는 레지스트리.
LangChain Tool 객체 또는 일반 callable 모두 등록 가능.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from app.core.config.loader import load_yaml

ToolCallable = Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        # tools.yml 이 없거나 비어 있어도 안전하게 처리
        try:
            data = load_yaml("tools") or {}
        except FileNotFoundError:
            data = {}

        # 예시: { "tools": { "current_time": {"enabled": true}, ... } }
        self._config: Dict[str, Dict[str, Any]] = data.get("tools", {})
        self._tools: Dict[str, ToolCallable] = {}

    # --------------------------
    # 등록
    # --------------------------
    def register(self, name: str, func: ToolCallable) -> None:
        """
        이름과 callable(또는 LangChain Tool 객체)을 레지스트리에 등록.
        """
        if name in self._tools:
            existing = self._tools[name]
            raise ValueError(
                f"Tool '{name}' is already registered. existing={existing}"
            )
        self._tools[name] = func

    # --------------------------
    # 조회
    # --------------------------
    def get(self, name: str) -> ToolCallable:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered")
        return self._tools[name]

    def list_all(self) -> Dict[str, ToolCallable]:
        """
        등록된 모든 툴 반환 (활성/비활성 포함).
        """
        return dict(self._tools)

    # --------------------------
    # 활성 툴 필터링
    # --------------------------
    def is_enabled(self, name: str) -> bool:
        cfg = self._config.get(name, {})
        # tools.yml 에 enabled 가 명시되지 않았으면 기본 True
        return cfg.get("enabled", True)

    def list_active_tools(self) -> Dict[str, ToolCallable]:
        """
        tools.yml 기준으로 enabled=True 인 툴만 반환 (dict 형태).
        """
        return {
            name: func
            for name, func in self._tools.items()
            if self.is_enabled(name)
        }

    def get_active_tool_list(self) -> list[ToolCallable]:
        """
        LangChain Agent 등에 바로 넘기기 좋은 list 형태.
        """
        return list(self.list_active_tools().values())


tool_registry = ToolRegistry()


def register_tool(name: Optional[str] = None):
    """
    함수/Tool 을 registry 에 자동 등록하는 데코레이터.

    @register_tool("current_time")
    def current_time_tool(...):
        ...
    """

    def decorator(func: ToolCallable) -> ToolCallable:
        tool_name = name or func.__name__
        tool_registry.register(tool_name, func)
        return func

    return decorator
