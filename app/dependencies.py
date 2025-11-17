# app/dependencies.py
"""
FastAPI Depends 로 공통 의존성 주입할 때 사용하는 모듈.
지금은 placeholder.
"""
from app.core.config.settings import settings


def get_settings():
    return settings
