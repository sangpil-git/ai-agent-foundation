# app/tools/builtin/time_tools.py
from datetime import datetime, timezone
from app.tools.base import registered_tool


@registered_tool("current_time", return_direct=True)
def current_time() -> str:
    """현재 UTC 시간을 ISO 8601 문자열로 반환"""
    return datetime.now(timezone.utc).isoformat()


@registered_tool("current_timestamp", return_direct=True)
def current_timestamp() -> float:
    """현재 Unix timestamp(초)를 반환"""
    return datetime.now().timestamp()
