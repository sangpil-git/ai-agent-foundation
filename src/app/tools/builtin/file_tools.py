# app/tools/builtin/file_tools.py
from pathlib import Path
from app.tools.base import registered_tool


@registered_tool("read_text_file")
def read_text_file(path: str) -> str:
    """
    텍스트 파일의 내용을 읽어서 반환.
    (보안상, 너무 긴 내용은 앞부분만 반환하게 할 수도 있음)
    """
    p = Path(path)
    if not p.exists() or not p.is_file():
        return f"[error] file not found: {path}"

    try:
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"[read_text_file error] {str(e)}"
