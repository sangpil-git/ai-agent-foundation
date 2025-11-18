# src/app/rag/embeddings/upstage_embedding.py
from typing import List
from app.rag.embeddings.base import BaseEmbedding
from app.core.config.settings import settings

# 예시: langchain-upstage 가 있다고 가정
from langchain_upstage import UpstageEmbeddings


class UpstageEmbedding(BaseEmbedding):
    def __init__(self, model: str | None = None):
        self.model = model or settings.UPSTAGE_EMBEDDING_MODEL
        self.client = UpstageEmbeddings(
            model=self.model,
            api_key=settings.UPSTAGE_API_KEY,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.client.embed_query(text)
