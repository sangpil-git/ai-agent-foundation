# app/utils/string.py
import re


def mask_sensitive(text: str, keep: int = 3) -> str:
    """
    문자열 민감정보 마스킹
    예: password -> pas****
    """
    if not text:
        return text
    return text[:keep] + "*" * (len(text) - keep)


def snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def camel_to_snake(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
