# src/app/resources/schema/model_schema.py
from pydantic import BaseModel
from typing import Dict, Optional


class ModelConfig(BaseModel):
    provider: str
    model: Optional[str] = None
    deployment: Optional[str] = None
    base_url: Optional[str] = None
    api_key_env: Optional[str] = None

    temperature: float | None = None
    max_tokens: int | None = None


class ModelsConfig(BaseModel):
    models: Dict[str, ModelConfig]
