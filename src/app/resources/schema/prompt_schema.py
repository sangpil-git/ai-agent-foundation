# config/schema/prompt_schema.py
from pydantic import BaseModel
from typing import Dict


class PromptsConfig(BaseModel):
    prompts: Dict[str, str]
