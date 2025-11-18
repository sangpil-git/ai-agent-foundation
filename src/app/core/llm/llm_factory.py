# app/core/llm_factory.py
"""
LLM 생성 팩토리.
- models.yml + settings 값을 기반으로
- provider(openai, gemini, anthropic, azure_openai, ollama)에 맞는 LLM 인스턴스 생성
"""
import os
from typing import Any, Optional

from app.core.config import settings
from app.core.llm.model_registry import model_registry, ModelConfig
from app.core.logging.logger import get_logger

logger = get_logger("llm_factory")


class LLMProviderNotAvailable(Exception):
    pass


def _resolve_api_key(cfg: ModelConfig) -> Optional[str]:
    """
    모델 설정의 api_key_env > settings.* 순으로 API 키를 찾아낸다.
    """
    if cfg.api_key_env:
        v = os.environ.get(cfg.api_key_env)
        if v:
            return v

    # fallback: settings에 있는 기본 값들
    provider = cfg.provider
    if provider == "openai":
        return settings.OPENAI_API_KEY
    if provider == "gemini":
        return settings.GOOGLE_API_KEY
    if provider == "anthropic":
        return settings.ANTHROPIC_API_KEY
    if provider == "azure_openai":
        return settings.AZURE_OPENAI_API_KEY

    return None


def _create_openai_llm(name: str, cfg: ModelConfig) -> Any:
    try:
        from langchain_openai import ChatOpenAI  # type: ignore
    except ImportError as e:
        raise LLMProviderNotAvailable(
            "langchain-openai 패키지가 필요합니다. `pip install langchain-openai`"
        ) from e

    api_key = _resolve_api_key(cfg)
    if not api_key:
        raise LLMProviderNotAvailable("OPENAI_API_KEY 가 설정되어 있지 않습니다.")

    model = cfg.model or name

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=cfg.temperature or 0.3,
        max_tokens=cfg.max_tokens,
    )


def _create_gemini_llm(name: str, cfg: ModelConfig) -> Any:
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
    except ImportError as e:
        raise LLMProviderNotAvailable(
            "langchain-google-genai 패키지가 필요합니다. `pip install langchain-google-genai`"
        ) from e

    api_key = _resolve_api_key(cfg)
    if not api_key:
        raise LLMProviderNotAvailable("GOOGLE_API_KEY 가 설정되어 있지 않습니다.")

    model = cfg.model or name

    return ChatGoogleGenerativeAI(
        model=model,
        api_key=api_key,
        temperature=cfg.temperature or 0.3,
        max_output_tokens=cfg.max_tokens,
    )


def _create_anthropic_llm(name: str, cfg: ModelConfig) -> Any:
    try:
        from langchain_anthropic import ChatAnthropic  # type: ignore
    except ImportError as e:
        raise LLMProviderNotAvailable(
            "langchain-anthropic 패키지가 필요합니다. `pip install langchain-anthropic`"
        ) from e

    api_key = _resolve_api_key(cfg)
    if not api_key:
        raise LLMProviderNotAvailable("ANTHROPIC_API_KEY 가 설정되어 있지 않습니다.")

    model = cfg.model or name

    return ChatAnthropic(
        model=model,
        api_key=api_key,
        temperature=cfg.temperature or 0.3,
        max_tokens=cfg.max_tokens,
    )


def _create_azure_openai_llm(name: str, cfg: ModelConfig) -> Any:
    try:
        from langchain_openai import AzureChatOpenAI  # type: ignore
    except ImportError as e:
        raise LLMProviderNotAvailable(
            "langchain-openai 패키지가 필요합니다. `pip install langchain-openai`"
        ) from e

    api_key = _resolve_api_key(cfg)
    if not api_key:
        raise LLMProviderNotAvailable("AZURE_OPENAI_API_KEY 가 설정되어 있지 않습니다.")

    deployment = cfg.deployment or settings.AZURE_OPENAI_DEPLOYMENT
    if not deployment:
        raise LLMProviderNotAvailable("Azure OpenAI deployment 이름이 설정되지 않았습니다.")

    endpoint = cfg.base_url or settings.AZURE_OPENAI_ENDPOINT
    if not endpoint:
        raise LLMProviderNotAvailable("AZURE_OPENAI_ENDPOINT 가 설정되지 않았습니다.")

    return AzureChatOpenAI(
        azure_deployment=deployment,
        api_key=api_key,
        azure_endpoint=endpoint,
        temperature=cfg.temperature or 0.3,
        max_tokens=cfg.max_tokens,
    )


def _create_ollama_llm(name: str, cfg: ModelConfig) -> Any:
    try:
        from langchain_community.chat_models import ChatOllama  # type: ignore
    except ImportError as e:
        raise LLMProviderNotAvailable(
            "langchain-community 패키지가 필요합니다. `pip install langchain-community`"
        ) from e

    base_url = cfg.base_url or settings.OLLAMA_BASE_URL
    model = cfg.model or name

    return ChatOllama(
        model=model,
        base_url=base_url,
        temperature=cfg.temperature or 0.3,
    )


def create_llm(model_name: Optional[str] = None) -> Any:
    """
    모델 이름 기반으로 LLM 인스턴스를 생성.
    - model_name 없으면 settings.OPENAI_MODEL 사용 (기본값)
    - models.yml에서 provider를 보고 해당 provider용 생성 함수 호출
    """
    if model_name is None:
        model_name = settings.OPENAI_MODEL

    cfg = model_registry.get(model_name)
    provider = cfg.provider.lower()

    logger.info(
        "create_llm",
        model_name=model_name,
        provider=provider,
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
    )

    if provider == "openai":
        return _create_openai_llm(model_name, cfg)
    if provider == "gemini":
        return _create_gemini_llm(model_name, cfg)
    if provider == "anthropic":
        return _create_anthropic_llm(model_name, cfg)
    if provider == "azure_openai":
        return _create_azure_openai_llm(model_name, cfg)
    if provider == "ollama":
        return _create_ollama_llm(model_name, cfg)

    # fallback: 아직 구현 안 된 provider
    raise LLMProviderNotAvailable(f"Unsupported provider: {provider}")
