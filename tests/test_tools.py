# tests/test_tools.py
from app.core.llm.tool_registry import tool_registry


def test_tool_registry_empty():
    tools = tool_registry.list_active_tools()
    assert isinstance(tools, dict)
