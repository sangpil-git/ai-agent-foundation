# app/rag/splitter/splitter_config.py
from dataclasses import dataclass

@dataclass
class TextSplitterConfig:
    chunk_size: int = 800
    chunk_overlap: int = 200
