# app/graphs/base/base_graph.py
"""
Graph 공통 베이스 클래스.

- LangGraph, LangChain Runnable 등 어떤 그래프/워크플로우든
  공통 인터페이스(BaseGraph)를 통해 감싸서 사용.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseGraph(ABC):
    """
    모든 Graph 구현체는 이 클래스를 상속해서 구현.
    """

    def preprocess(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """그래프 실행 전 데이터 전처리"""
        return input_data

    @abstractmethod
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """그래프 핵심 실행"""
        raise NotImplementedError

    def postprocess(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """그래프 실행 후 후처리"""
        return result

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = self.preprocess(input_data)
        result = self.run(data)
        output = self.postprocess(result)
        return output
