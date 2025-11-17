# app/utils/json.py
import json


def safe_json(data) -> str:
    try:
        return json.dumps(data, ensure_ascii=False)
    except Exception:
        return "{}"


def pretty_json(data) -> str:
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception:
        return "{}"
