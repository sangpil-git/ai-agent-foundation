# app/chains/builtin/summarize_chain.py

from __future__ import annotations

from typing import Any, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.base.base_chain import BaseChain, ChainInput, ChainOutput
from app.chains.base.chain_registry import register_chain
from app.core.llm import create_llm, prompt_registry
from app.core.llm.prompt_to_messages import convert_prompt_to_messages


@register_chain("summarize")
class SummarizeChain(BaseChain):
    def __init__(self, model_name: Optional[str] = None) -> None:
        super().__init__(name="SummarizeChain")

        self.model_name = model_name
        self.llm = create_llm(model_name)  # model_name=None 이면 settings 기본값 사용

        prompt_conf = prompt_registry.get(
            task="summarize",
            role="assistant",
            user_prompt={"input": "{input}"},
        )

        messages = convert_prompt_to_messages(prompt_conf)
        self.prompt = ChatPromptTemplate.from_messages(messages)
        self.chain = self.prompt | self.llm | StrOutputParser()

    def validate_input(self, input_data: ChainInput) -> None:
        raw_text: Any = input_data.get("text", None)

        if raw_text is None:
            raise ValueError("'text' 필드는 반드시 필요합니다.")
        if not isinstance(raw_text, str):
            raise ValueError("요약할 'text' 값은 문자열(str)이어야 합니다.")
        if not raw_text.strip():
            raise ValueError("요약할 'text' 값은 비어 있을 수 없습니다.")

    def preprocess(self, input_data: ChainInput) -> ChainInput:
        text = input_data["text"].strip()
        # 나머지 메타 데이터도 유지
        return {**input_data, "text": text}

    def run(self, data: ChainInput) -> ChainOutput:
        text = data["text"]
        output = self.chain.invoke({"input": text})

        return {
            "model": self.model_name,
            "output": output,
        }

    def postprocess(self, result: ChainOutput) -> ChainOutput:
        result.setdefault("model", self.model_name)
        result.setdefault("output", "")
        return result
