from typing import Callable, Dict, Any

from agents.echo_agent.chain import build_echo_chain
from agents.echo_agent.graph import build_echo_graph
from agents.rag_agent.chain import build_rag_chain

AgentFactory = Callable[[], Any]

AGENT_REGISTRY: Dict[str, AgentFactory] = {
    "echo_chain": build_echo_chain,
    "echo_graph": build_echo_graph,
    "rag_chain": build_rag_chain,
    # "planner_executor": ... 나중에 추가
}


def get_agent(name: str):
    factory = AGENT_REGISTRY.get(name)
    if not factory:
        raise ValueError(f"Unknown agent: {name}")
    return factory()
