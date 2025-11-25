# app/rag/pipeline/pipeline_config.py
from dataclasses import dataclass

@dataclass
class RagIndexConfig:
    persist_directory: str = "data/chroma"
    collection_name: str = "default"
    chunk_size: int = 800
    chunk_overlap: int = 200
