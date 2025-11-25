# app/tools/builtin/web_tools.py
import requests
from app.tools.base import registered_tool


@registered_tool("http_get")
def http_get(url: str, timeout: int = 5) -> str:
    """
    단순 HTTP GET 요청.
    응답 body 텍스트를 반환.
    """
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return f"[http_get error] {str(e)}"
