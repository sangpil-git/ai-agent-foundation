# app/chains/echo_chain.py
"""
아주 기본적인 Echo 체인 예시.
"""
from typing import Any, Dict

from app.chains.base.base_chain import BaseChain
from app.chains.base.chain_registry import register_chain


@register_chain("echo")
class EchoChain(BaseChain):
    """
    input_data 자체를 그대로 되돌려주거나,
    일부 필드만 echo 해주는 간단 체인.
    """

    def __init__(self, model_name: str | None = None):
        # model_name 을 받긴 하지만, 이 체인은 실제 사용하진 않음
        self.model_name = model_name

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        text = input_data.get("text", "")
        return {
            "output": text,
        }
