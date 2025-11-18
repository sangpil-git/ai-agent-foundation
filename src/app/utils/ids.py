# app/utils/ids.py
import uuid
import secrets
import string


def uuid4() -> str:
    return str(uuid.uuid4())


def short_id(length: int = 12) -> str:
    """
    URL-safe 짧은 ID (nanoid 대체)
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_request_id() -> str:
    return f"req_{short_id(10)}"
