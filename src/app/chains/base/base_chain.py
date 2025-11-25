# app/chains/base/base_chain.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

from app.core.exceptions import AppError

ChainInput = Dict[str, Any]
ChainOutput = Dict[str, Any]


class BaseChain(ABC):
    """
    Chain 공통 베이스 클래스.
    Chain과 Graph 모두 동일한 인터페이스를 사용하도록 설계됨.
    """

    def __init__(self, name: Optional[str] = None) -> None:
        self._name = name or self.__class__.__name__
        self.logger = logging.getLogger(self._name)

    @property
    def name(self) -> str:
        return self._name

    # --------------------------
    # 1) 입력 검증
    # --------------------------
    def validate_input(self, input_data: ChainInput) -> None:
        return

    # --------------------------
    # 2) 전처리
    # --------------------------
    def preprocess(self, input_data: ChainInput) -> ChainInput:
        return input_data

    # --------------------------
    # 3) 핵심 실행 (필수)
    # --------------------------
    @abstractmethod
    def run(self, data: ChainInput) -> ChainOutput:
        raise NotImplementedError

    # --------------------------
    # 4) 후처리
    # --------------------------
    def postprocess(self, result: ChainOutput) -> ChainOutput:
        return result

    # --------------------------
    # 공통 entry-point
    # --------------------------
    def invoke(self, input_data: ChainInput) -> ChainOutput:
        try:
            self.validate_input(input_data)
            processed = self.preprocess(input_data)
            result = self.run(processed)
            return self.postprocess(result)
        
        except AppError:
            # 커스텀 에러는 그대로 외부로 전달
            raise

        except Exception as e:
            raise AppError(str(e), code="chain_unexpected_error") from e

    async def ainvoke(self, input_data: ChainInput) -> ChainOutput:
        return self.invoke(input_data)

    def __call__(self, input_data: ChainInput) -> ChainOutput:
        return self.invoke(input_data)
