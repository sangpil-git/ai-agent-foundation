from typing import Protocol, List, Dict, Any
from collections import defaultdict
from dataclasses import dataclass

from langchain_core.messages import BaseMessage, AIMessage, HumanMessage


class ConversationMemory(Protocol):
    async def add(self, session_id: str, message: BaseMessage) -> None: ...
    async def get_history(self, session_id: str) -> List[BaseMessage]: ...


@dataclass
class InMemoryConversationMemory(ConversationMemory):
    store: Dict[str, List[BaseMessage]]

    def __init__(self):
        self.store = defaultdict(list)

    async def add(self, session_id: str, message: BaseMessage) -> None:
        self.store[session_id].append(message)

    async def get_history(self, session_id: str) -> List[BaseMessage]:
        return self.store.get(session_id, [])


# TODO: Redis 백엔드, DB 백엔드 등 확장
# class RedisConversationMemory(ConversationMemory): ...


# 간단 팩토리
from core.config import settings


def get_memory_backend() -> ConversationMemory:
    if settings.MEMORY_BACKEND == "inmemory":
        return InMemoryConversationMemory()
    # elif settings.MEMORY_BACKEND == "redis":
    #     return RedisConversationMemory(...)
    else:
        return InMemoryConversationMemory()
