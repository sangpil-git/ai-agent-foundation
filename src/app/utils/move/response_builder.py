# app/utils/response_builder.py

from typing import Any, Optional


def success_response(data: Any) -> dict:
    return {
        "success": True,
        "data": data,
        "error": None
    }


def error_response(message: str, code: Optional[str] = None) -> dict:
    return {
        "success": False,
        "data": None,
        "error": {
            "message": message,
            "code": code,
        }
    }
