# app/tools/base.py
"""
공통 Tool 베이스/타입 정의.
LangChain tool 과 registry 연동용 helper.
"""
from typing import Any, Callable, Optional
from langchain_core.tools import tool as lc_tool

from app.tools.tool_registry import register_tool


def registered_tool(name: Optional[str] = None, **lc_kwargs):
    """
    LangChain tool + registry.register 를 한 번에 적용하는 데코레이터.

    예:
    @registered_tool("current_time", return_direct=True)
    def current_time(...):
        ...
    """

    def decorator(func: Callable[..., Any]):
        tool_name = name or func.__name__
        # langchain tool wrapping
        wrapped = lc_tool(**lc_kwargs)(func)
        # registry 에도 등록
        register_tool(tool_name)(wrapped)
        return wrapped

    return decorator
