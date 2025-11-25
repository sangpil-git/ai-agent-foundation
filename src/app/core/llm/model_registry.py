# app/core/model_registry.py
from typing import Dict

from app.resources.schema.model_schema import ModelsConfig, ModelConfig
from app.core.config.loader import load_yaml


class ModelRegistry:
    def __init__(self) -> None:
        data = load_yaml("models")

        print("Loaded model registry data:", data)
        if not data:
            self._models: Dict[str, ModelConfig] = {}
        else:
            cfg = ModelsConfig(**data)
            self._models = cfg.models

    def list_models(self) -> Dict[str, ModelConfig]:
        return self._models

    def get(self, name: str) -> ModelConfig:
        if name not in self._models:
            raise KeyError(f"Model '{name}' not found in registry")
        return self._models[name]


model_registry = ModelRegistry()
