# app/chains/summarize_chain.py
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.base.base_chain import BaseChain
from app.chains.base.chain_registry import register_chain
from app.core.llm import create_llm, prompt_registry
from app.core.llm.prompt_to_messages import convert_prompt_to_messages


@register_chain("summarize")
class SummarizeChain(BaseChain):
    """
    텍스트 요약 체인.
    - LLM: create_llm(model_name)으로 생성 (provider는 models.yml + settings 기준)
    - Prompt: prompts.yml의 task=summary + role=assistant 기반
    - BaseChain의 preprocess → run → postprocess 3단계를 사용
    """

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name
        self.llm = create_llm(model_name)

        # prompts.yml 에서 summarize + assistant 프롬프트 병합
        # user_prompt 에서 {input} 변수를 쓴다고 가정
        prompt_conf = prompt_registry.get(
            task="summarize",
            role="assistant",
            user_prompt={"input": "{input}"},
        )

        messages = convert_prompt_to_messages(prompt_conf)
        self.prompt = ChatPromptTemplate.from_messages(messages)

        # Runnable 체인
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    # -------------------------------------------------
    # 입력 전처리
    # -------------------------------------------------
    def preprocess(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        input_data 예:
        {
          "text": "요약할 텍스트 ..."
        }
        """
        raw_text: Any = input_data.get("text", "")

        if not isinstance(raw_text, str):
            raise ValueError("요약할 text 값은 문자열(str)이어야 합니다.")

        text = raw_text.strip()
        if not text:
            raise ValueError("요약할 text 값은 비어 있을 수 없습니다.")

        # run 단계에서 쓰기 좋게 정규화된 형태로 반환
        return {"text": text}
    
    # -------------------------------------------------
    # 핵심 실행
    # -------------------------------------------------
    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        - BaseChain.invoke() 에서 preprocess 후 넘어온 data 를 사용
        - self.chain.invoke() 에는 {input: ...} 형태로 전달
        """
        text = data["text"]

        # 위에서 {input} 변수를 썼으므로, invoke 시에도 input 키로 전달
        output = self.chain.invoke({"input": text})

        # postprocess 에서 최종 포맷을 바꾸기 쉽게 중간 형태로 반환해도 되지만,
        # 여기서는 거의 최종 형태에 가깝게 맞춰서 반환
        return {
            "model": self.model_name,
            "output": output,
        }

    # -------------------------------------------------
    # ③ 후처리 (필요하면 확장, 지금은 그대로 반환)
    # -------------------------------------------------
    def postprocess(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        - 나중에 로그 메타데이터 붙이거나 형식을 바꾸고 싶을 때 여기서 처리.
        - 지금은 그대로 반환.
        """
        return result
