# src/app/graphs/base/graph_types.py
from __future__ import annotations

from typing import List, TypedDict
from typing_extensions import Annotated
import operator

from langchain_core.documents import Document


class BaseGraphState(TypedDict, total=False):
    """
    그래프에서 공통으로 쓸 수 있는 state 기본 골격.
    - 필요한 그래프에서 이 TypedDict을 상속해서 필드 추가.
    """
    question: str
    answer: str
    context_docs: List[Document]

    # messages 예시 (ChatBot 스타일 그래프 만들 때 사용 가능)
    # messages: Annotated[List[BaseMessage], operator.add]
