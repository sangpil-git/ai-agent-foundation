# app/tools/base.py
"""
공통 Tool 베이스/타입 정의.
LangChain tool 과 registry 연동용 helper.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, TypeVar, ParamSpec

from langchain_core.tools import tool as lc_tool

from app.tools.tool_registry import register_tool

P = ParamSpec("P")
R = TypeVar("R")


def registered_tool(name: Optional[str] = None, **lc_kwargs):
    """
    LangChain tool + registry.register 를 한 번에 적용하는 데코레이터.

    예:
    @registered_tool("current_time", return_direct=True)
    def current_time(...):
        ...
    """

    def decorator(func: Callable[P, R]) -> Callable[..., Any]:
        tool_name = name or func.__name__

        # LangChain tool wrapping
        # langchain_core.tools.tool 은 name= 키워드를 받지 않고,
        # 첫 번째 위치 인자로 이름을 받는 패턴을 사용.
        wrapped = lc_tool(tool_name, **lc_kwargs)(func)

        # registry 에 LangChain Tool 객체 등록
        register_tool(tool_name)(wrapped)

        return wrapped

    return decorator
