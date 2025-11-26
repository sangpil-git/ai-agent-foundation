# app/graphs/base/base_graph.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

from langgraph.types import RunnableConfig
from app.core.exceptions import AppError


GraphInput = Dict[str, Any]
GraphOutput = Dict[str, Any]


class BaseGraph(ABC):
    """
    모든 Graph의 공통 베이스 클래스.
    Chain과 구조/단계/메서드명을 동일하게 맞춘 버전.
    """

    def __init__(self, name: Optional[str] = None) -> None:
        self._name = name or self.__class__.__name__
        self.logger = logging.getLogger(self._name)
        self._compiled = None

    @property
    def name(self) -> str:
        return self._name

    # --------------------------
    # 그래프 빌드 (필수)
    # --------------------------
    @abstractmethod
    def build(self):
        raise NotImplementedError

    @property
    def compiled(self):
        if self._compiled is None:
            self._compiled = self.build()
        return self._compiled

    # --------------------------
    # 1) 입력 검증
    # --------------------------
    def validate_input(self, input_data: GraphInput) -> None:
        return

    # --------------------------
    # 2) 전처리
    # --------------------------
    def preprocess(self, input_data: GraphInput) -> GraphInput:
        return input_data

    # --------------------------
    # 3) 핵심 실행 (Chain과 동일한 이름 run 사용)
    # --------------------------
    def run(
        self,
        data: GraphInput,
        config: Optional[RunnableConfig] = None,
    ) -> GraphOutput:
        """
        Chain의 run()과 동일한 이름.
        내부에서는 Graph의 compiled.invoke(data)를 실행.
        """
        if config is not None:
            return self.compiled.invoke(data, config=config)
        return self.compiled.invoke(data)

    # --------------------------
    # 4) 후처리
    # --------------------------
    def postprocess(self, result: GraphOutput) -> GraphOutput:
        return result

    # --------------------------
    # 통합 entry-point
    # --------------------------
    def invoke(
        self,
        input_data: GraphInput,
        config: Optional[RunnableConfig] = None,
    ) -> GraphOutput:
        try:
            # 1) 입력 검증
            self.validate_input(input_data)
            # 2) 전처리
            processed = self.preprocess(input_data)
            # 3) 그래프 실행
            result = self.run(processed, config=config)
            # 4) 후처리
            return self.postprocess(result)

        except AppError:
            raise

        except Exception as e:
            raise AppError(str(e), code="graph_unexpected_error") from e

    async def ainvoke(
        self,
        input_data: GraphInput,
        config: Optional[RunnableConfig] = None,
    ) -> GraphOutput:
        return self.invoke(input_data, config=config)

    def __call__(self, input_data: GraphInput):
        return self.invoke(input_data)
