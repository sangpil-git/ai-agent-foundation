# app/tools/time_tools.py
from datetime import datetime
from app.tools.base import registered_tool


@registered_tool("current_time")
def current_time_tool() -> str:
    """
    현재 시간을 ISO 형식 문자열로 반환하는 간단한 툴.
    """
    return datetime.now().isoformat()
