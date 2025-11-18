# src/app/rag/embeddings/openai_embedding.py
from typing import List
from langchain_openai import OpenAIEmbeddings

from app.rag.embeddings.base import BaseEmbedding
from app.core.config.settings import settings


class OpenAIEmbedding(BaseEmbedding):
    def __init__(self, model: str | None = None):
        self.model = model or settings.EMBEDDING_MODEL
        self.client = OpenAIEmbeddings(
            model=self.model,
            api_key=settings.OPENAI_API_KEY,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.client.embed_query(text)
