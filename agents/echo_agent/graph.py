from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from core.llm import get_chat_model


class EchoState(TypedDict):
    input: str
    output: str


def _call_model(state: EchoState) -> EchoState:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant (LangGraph). Echo user input."),
            ("user", "{input}"),
        ]
    )
    llm = get_chat_model()
    runnable: Runnable = prompt | llm | StrOutputParser()
    result = runnable.invoke({"input": state["input"]})
    return {"input": state["input"], "output": result}


def build_echo_graph():
    graph = StateGraph(EchoState)
    graph.add_node("call_model", _call_model)
    graph.set_entry_point("call_model")
    graph.add_edge("call_model", END)
    app = graph.compile()
    return app
