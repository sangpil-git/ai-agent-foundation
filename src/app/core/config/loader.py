# app/core/config_loader.py
"""
YAML 설정(models.yml, prompts.yml, tools.yml 등)을 로딩하는 헬퍼.
추후 pydantic schema 검증 로직 추가 예정.
"""
from pathlib import Path
from typing import Any, Dict
import yaml

from app.core.config.settings import BASE_DIR


CONFIG_DIR = BASE_DIR / "config"


def load_yaml(name: str) -> Dict[str, Any]:
    """
    config/{name}.yml 파일 로딩.
    """
    path = CONFIG_DIR / f"{name}.yml"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
