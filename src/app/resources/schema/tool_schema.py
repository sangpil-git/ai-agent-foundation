# config/schema/tool_schema.py
from pydantic import BaseModel
from typing import Dict


class ToolEntry(BaseModel):
    enabled: bool = True


class ToolsConfig(BaseModel):
    tools: Dict[str, ToolEntry]
