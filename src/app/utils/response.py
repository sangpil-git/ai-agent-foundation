# app/utils/response.py

from __future__ import annotations
from typing import Any, Optional


def success_response(data: Any) -> dict:
    """
    API 성공 응답의 최소 포맷.
    """
    return {
        "success": True,
        "data": data,
        "error": None,
    }


def error_response(message: str, code: Optional[str] = None) -> dict:
    """
    API 실패 응답의 최소 포맷.
    """
    return {
        "success": False,
        "data": None,
        "error": {
            "message": message,
            "code": code or "ERROR",
        },
    }
