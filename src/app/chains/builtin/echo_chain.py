# app/chains/builtin/echo_chain.py

from __future__ import annotations

from app.chains.base.base_chain import BaseChain, ChainInput, ChainOutput
from app.chains.base.chain_registry import register_chain


@register_chain("echo")
class EchoChain(BaseChain):
    """
    가장 단순한 Echo 체인.
    - 입력: { "text": "hello" }
    - 출력: { "output": "hello" }
    """

    def __init__(self, model_name: str | None = None) -> None:
        super().__init__(name="EchoChain")
        self.model_name = model_name  # 시그니처 통일 목적

    def validate_input(self, input_data: ChainInput) -> None:
        if "text" not in input_data:
            raise ValueError("'text' 필드는 반드시 필요합니다.")

    def run(self, data: ChainInput) -> ChainOutput:
        return {"output": data.get("text", "")}
