# app/middleware/request_logging.py
from __future__ import annotations

import time
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.logging.logger import get_logger

logger = get_logger("request")


def _mask_query_string(query: str) -> str:
    """
    쿼리스트링에서 토큰/패스워드 등 민감 키를 간단히 마스킹.
    필요 시 키 목록을 늘리거나, 정규식으로 강화 가능.
    """
    SENSITIVE_KEYS = {"token", "access_token", "refresh_token", "password", "pwd"}
    if not query:
        return query

    parts: list[str] = []
    for kv in query.split("&"):
        if "=" not in kv:
            parts.append(kv)
            continue
        k, v = kv.split("=", 1)
        if k.lower() in SENSITIVE_KEYS:
            parts.append(f"{k}=***")
        else:
            parts.append(kv)
    return "&".join(parts)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    HTTP Request/Response 로깅 미들웨어

    - method, path, query, status_code, 처리시간(ms), client ip, user-agent 로그
    - request/response body 는 기본적으로 로깅하지 않음 (성능/보안 이슈)
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()

        client_host = request.client.host if request.client else "-"
        method = request.method
        url_path = request.url.path
        raw_query = str(request.url.query)
        query = _mask_query_string(raw_query)
        user_agent = request.headers.get("user-agent", "-")

        # 공통 라인 한 번만 생성 (중복 제거)
        request_line = f"{client_host} {method} {url_path}"
        if query:
            request_line += f"?{query}"

        logger.info(
            f"[REQUEST] {request_line} UA={user_agent}"
        )

        # response 생성
        response = await call_next(request)

        process_time_ms = (time.time() - start_time) * 1000.0
        status_code = response.status_code

        logger.info(
            f"[RESPONSE] {request_line} -> {status_code} ({process_time_ms:.2f} ms)"
        )

        return response
