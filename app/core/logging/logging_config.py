# app/core/logging_config.py
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

import structlog
from app.core.config import settings

LOG_DIR = Path(__file__).resolve().parents[3] / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.json"

def setup_logging() -> None:
    """
    structlog + 기본 logging 글로벌 설정
    - LOG_LEVEL (DEBUG/INFO/WARNING/ERROR/CRITICAL) 전역 적용
    """
    # ─────────────────────────────────────────────────────────
    # LOG LEVEL 가져오기
    # ─────────────────────────────────────────────────────────
    log_level_name = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    # ─────────────────────────────────────────────────────────
    # Python 기본 로깅 설정
    # ─────────────────────────────────────────────────────────
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(log_level)

    formatter = logging.Formatter("%(message)s")

    # Console
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(log_level)
    console.setFormatter(formatter)
    root_logger.addHandler(console)

    # File (JSON output)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=20 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    root_logger.addHandler(file_handler)

    # ─────────────────────────────────────────────────────────
    # structlog 설정
    # ─────────────────────────────────────────────────────────
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    print(f"🔧 Logging initialized with LOG_LEVEL={log_level_name}, file={LOG_FILE}")
