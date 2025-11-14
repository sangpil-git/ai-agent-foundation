# agents/echo_agent/chain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser

from core.llm import get_chat_model


def build_echo_chain() -> Runnable:
    """
    LangChain Runnable 기반 에코 체인.
    - system: 역할 정의
    - user: 입력 그대로 반사 + 약간 포맷팅
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Repeat user input with a friendly explanation.",
            ),
            ("user", "{input}"),
        ]
    )

    llm = get_chat_model()
    chain: Runnable = prompt | llm | StrOutputParser()
    return chain
