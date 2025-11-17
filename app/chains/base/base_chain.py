# app/chains/base_chain.py
"""
Chain 공통 베이스 클래스.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseChain(ABC):
    """
    모든 체인은 이 클래스를 상속해서 구현.
    """

    # --------------------------
    # 입력 전처리
    # --------------------------
    def preprocess(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """체인 실행 전 공통 전처리 단계"""
        return input_data

    # --------------------------
    # 핵심 실행 (반드시 구현)
    # --------------------------
    @abstractmethod
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """체인의 핵심 로직"""
        raise NotImplementedError

    # --------------------------
    # 후처리
    # --------------------------
    def postprocess(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """체인 실행 후 후처리 단계"""
        return result

    # --------------------------
    # 외부에서 호출하는 entry-point
    # --------------------------
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """전체 파이프라인 구성"""
        data = self.preprocess(input_data)
        result = self.run(data)
        output = self.postprocess(result)
        return output
