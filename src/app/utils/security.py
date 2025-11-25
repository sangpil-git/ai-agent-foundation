# app/utils/security.py

from __future__ import annotations
import hashlib
import hmac


def sha256(text: str) -> str:
    """
    문자열을 SHA256 해시로 변환.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hmac_sha256(secret: str, message: str) -> str:
    """
    HMAC-SHA256 서명 생성.
    - secret: 키
    - message: 메시지 본문
    """
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
