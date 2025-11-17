# app/utils/time.py
from datetime import datetime, timezone, timedelta


def now() -> datetime:
    return datetime.now(timezone.utc)


def timestamp_ms() -> int:
    return int(now().timestamp() * 1000)


def format_iso(dt: datetime | None = None):
    dt = dt or now()
    return dt.astimezone(timezone.utc).isoformat()


def measure_time_ms(func):
    """
    함수 실행시간 측정 decorator
    """
    def wrapper(*args, **kwargs):
        start = timestamp_ms()
        result = func(*args, **kwargs)
        end = timestamp_ms()
        return result, (end - start)
    return wrapper
