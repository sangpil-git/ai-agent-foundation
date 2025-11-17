# app/utils/exceptions.py
class AppError(Exception):
    """
    모든 커스텀 에러의 base
    """
    def __init__(self, message: str, code: str = "app_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationError(AppError):
    def __init__(self, message="Validation failed"):
        super().__init__(message, code="validation_error")


class ExternalAPIError(AppError):
    def __init__(self, message="External API call failed"):
        super().__init__(message, code="external_api_error")


class RAGError(AppError):
    def __init__(self, message="RAG processing failed"):
        super().__init__(message, code="rag_error")
