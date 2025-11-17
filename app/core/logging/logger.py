# app/core/logger.py
import structlog


def get_logger(name: str = None):
    """
    글로벌 공용 JSON logger
    """
    return structlog.get_logger(name)
