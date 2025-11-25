# app/core/exceptions.py

from __future__ import annotations


class AppError(Exception):
    """
    모든 커스텀 에러의 base 클래스.
    - message: 오류 설명
    - code: 시스템 내부 에러 코드
    """
    def __init__(self, message: str, code: str = "app_error"):
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationError(AppError):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, code="validation_error")


class ExternalAPIError(AppError):
    def __init__(self, message: str = "External API call failed"):
        super().__init__(message, code="external_api_error")


class RAGError(AppError):
    def __init__(self, message: str = "RAG processing failed"):
        super().__init__(message, code="rag_error")
