# app/core/config_loader.py
"""
YAML 설정(models.yml, prompts.yml, tools.yml 등)을 로딩하는 헬퍼.
추후 pydantic schema 검증 로직 추가 예정.
"""
from pathlib import Path
from typing import Any, Dict
import yaml

from app.core.config.settings import RESOURCE_DIR

def load_yaml(name: str) -> Dict[str, Any]:
    """
    resource/{name}.yml 파일 로딩.
    """
    path = RESOURCE_DIR / f"{name}.yml"

    print("Loading YAML file:", path)

    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
