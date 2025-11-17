# core/langsmith_config.py
import os
from typing import List, Optional


from langchain_core.callbacks import BaseCallbackHandler
from app.core.config.settings import settings
from app.core.logging import logger

_LANGSMITH_INITIALIZED = False


def init_langsmith(
    project_name: Optional[str] = None,
    enabled: bool = True,
) -> None:
    """
    LangSmith / LangChain 트레이싱 초기화
    - enabled: True 기준 (기본값)
    - project_name: 없으면 settings.LANGSMITH_PROJECT 사용
    """

    global _LANGSMITH_INITIALIZED
    if _LANGSMITH_INITIALIZED:
        return

    # 비활성화 옵션
    if not enabled:
        os.environ["LANGSMITH_TRACING"] = "false"
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        _LANGSMITH_INITIALIZED = True
        print("🚫 LangSmith tracing disabled.")
        return

    # API Key 확인 (settings 우선, 없으면 env)
    api_key = settings.LANGSMITH_API_KEY or os.environ.get("LANGSMITH_API_KEY")
    if not api_key:
        print(
            "⚠️ LANGSMITH_API_KEY 가 설정되지 않아 LangSmith 트레이싱을 활성화할 수 없습니다."
        )
        _LANGSMITH_INITIALIZED = True
        return

    # 프로젝트명 결정
    project = project_name or settings.LANGSMITH_PROJECT or "agent-foundation"

    # LangChain v2 트레이싱 플래그
    # os.environ["LANGCHAIN_TRACING_V2"] = "true"

    # LangSmith 호환 플래그
    os.environ["LANGSMITH_TRACING"] = "true"

    # API 키
    os.environ["LANGSMITH_API_KEY"] = api_key

    # 프로젝트명
    os.environ["LANGSMITH_PROJECT"] = project

    # 엔드포인트
    endpoint = settings.LANGSMITH_ENDPOINT or "https://api.smith.langchain.com"
    os.environ["LANGSMITH_ENDPOINT"] = endpoint

    print(f"✅ LangSmith tracing enabled: project={project}")
    _LANGSMITH_INITIALIZED = True


def get_default_callbacks() -> List[BaseCallbackHandler]:
    """
    LangChain 최신 권장 방식에 맞춰 콜백은 기본적으로 비워둠.
    - init_langsmith() 만 호출되어 있으면 자동으로 LangSmith에 트레이싱 전송됨.
    """
    init_langsmith()  # 기본값: enabled=True, project=settings 값
    return []
