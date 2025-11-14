from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

from core.config import settings


def get_chat_model(
    model_name: str | None = None,
    temperature: float = 0.1,
) -> BaseChatModel:
    """
    LLM 공급자별로 공통 인터페이스 반환.
    나중에 Anthropic, Azure OpenAI 등도 여기서 스위칭.
    """
    if settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model=model_name or settings.OPENAI_MODEL,
            temperature=temperature,
        )
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}")
