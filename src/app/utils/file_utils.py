# app/utils/file.py
from pathlib import Path


def read_file(path: str | Path, default="") -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception:
        return default


def write_file(path: str | Path, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
