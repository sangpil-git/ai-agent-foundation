# app/core/tool_registry.py
"""
tools.yml 에 정의된 툴들을 코드 상의 함수/객체와 매핑하는 레지스트리.
"""
from typing import Callable, Dict, Any, Optional

from app.core.config.loader import load_yaml


class ToolRegistry:
    def __init__(self) -> None:
        data = load_yaml("tools")
        # 예시: { "tools": { "current_time": {"enabled": true}, ... } }
        self._config = data.get("tools", {})
        self._tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]) -> None:
        self._tools[name] = func

    def get(self, name: str) -> Callable[..., Any]:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered")
        return self._tools[name]

    def list_active_tools(self) -> Dict[str, Callable[..., Any]]:
        active = {}
        for name, func in self._tools.items():
            cfg = self._config.get(name, {})
            if cfg.get("enabled", True):
                active[name] = func
        return active


tool_registry = ToolRegistry()

def register_tool(name: Optional[str] = None):
    """
    함수/Tool 을 registry 에 자동 등록하는 데코레이터.

    @register_tool("current_time")
    def current_time_tool(...):
        ...
    """
    def decorator(func: Callable[..., Any]):
        tool_name = name or func.__name__
        tool_registry.register(tool_name, func)
        return func
    return decorator
