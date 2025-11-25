# app/middleware/error_handler.py
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError
from app.utils.response import error_response
from app.core.logging.logger import get_logger

logger = get_logger("error")


async def app_error_handler(request: Request, exc: AppError):
    """
    우리가 정의한 AppError 계열 예외 처리.
    """
    logger.warning(
        "AppError occurred",
        extra={
            "path": request.url.path,
            "code": exc.code,
            "message": exc.message,
        },
    )
    return JSONResponse(
        status_code=400,
        content=error_response(message=exc.message, code=exc.code),
    )


async def unhandled_error_handler(request: Request, exc: Exception):
    """
    예기치 못한 모든 예외 처리 (fallback).
    """
    logger.exception(
        "Unhandled exception",
        extra={"path": request.url.path},
    )
    return JSONResponse(
        status_code=500,
        content=error_response(
            message="Internal server error",
            code="internal_error",
        ),
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """
    FastAPI 앱에 예외 핸들러를 등록하는 helper.
    main.py 등에서 호출:
      setup_exception_handlers(app)
    """
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
