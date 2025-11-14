from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

from core.llm import get_chat_model
from tools.db_knowledge import db_knowledge_search


def build_rag_chain() -> Runnable:
    """
    - user 질문을 입력받고
    - RAG 검색(db_knowledge_search tool) 수행 결과 + 질문 → LLM 답변
    """

    # 1) RAG 검색 + 원 질문을 병렬 처리
    def _retrieve(question: str) -> dict:
        context = db_knowledge_search.invoke({"query": question})
        return {"context": context, "question": question}

    # 2) Prompt 템플릿
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "당신은 사내 지식 기반 RAG 어시스턴트입니다.\n"
                    "주어진 context를 우선적으로 참고하여 답변하세요.\n"
                    "context에 없으면 추론임을 명시해주세요."
                ),
            ),
            ("system", "context:\n{context}"),
            ("user", "{question}"),
        ]
    )

    llm = get_chat_model()

    chain: Runnable = (
        RunnableParallel(
            context=lambda x: db_knowledge_search.invoke(
                {"query": x["input"]["question"]}
            ),
            question=lambda x: x["input"]["question"],
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
