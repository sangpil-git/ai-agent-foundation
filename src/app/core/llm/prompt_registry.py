# app/core/llm/prompt_registry.py
from typing import Dict, Optional
from app.core.config.loader import load_yaml
from app.core.logging import get_logger

logger = get_logger("prompt_registry")


class PromptRegistry:
    def __init__(self):
        self._prompts = load_yaml("config/prompts.yml")

        self.default = self._prompts.get("default", {})
        self.tasks = self._prompts.get("tasks", {})
        self.roles = self._prompts.get("roles", {})
        self.custom = self._prompts.get("custom", {})

    # ------------------------------------
    # 사용자 정의 프롬프트 추가
    # ------------------------------------
    def add_custom(self, name: str, prompt: Dict):
        self.custom[name] = prompt
        logger.info("Custom prompt added", name=name)

    # ------------------------------------
    # 프롬프트 병합
    # ------------------------------------
    def merge_prompts(self, *keys) -> Dict:
        merged = {}

        for key in keys:
            if key is None:
                continue

            if isinstance(key, dict):
                merged.update(key)
            elif key in self.tasks:
                merged.update(self.tasks[key])
            elif key in self.roles:
                merged.update(self.roles[key])
            elif key in self.custom:
                merged.update(self.custom[key])
            else:
                logger.warning("Unknown prompt key", key=key)

        return merged

    # ------------------------------------
    # 프롬프트 가져오기
    # ------------------------------------
    def get(self, 
            task: Optional[str] = None,
            role: Optional[str] = None,
            user_prompt: Optional[Dict] = None) -> Dict:
        
        merged = {}

        # 1. default prompt
        merged.update(self.default)

        # 2. task-level
        if task and task in self.tasks:
            merged.update(self.tasks[task])

        # 3. role-level
        if role and role in self.roles:
            merged.update(self.roles[role])

        # 4. custom user-level
        if user_prompt:
            merged.update(user_prompt)

        return merged


prompt_registry = PromptRegistry()
