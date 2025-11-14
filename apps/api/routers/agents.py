from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Literal, Optional, Union

from agents import get_agent

router = APIRouter()


class AgentInvokeRequest(BaseModel):
    input: Union[str, Dict[str, Any]]
    mode: Literal["chain", "graph"] = "chain"
    session_id: Optional[str] = None  # memory 연동 시 확장 포인트


@router.post("/{agent_name}/invoke")
async def invoke_agent(agent_name: str, body: AgentInvokeRequest):
    try:
        agent = get_agent(agent_name)
    except ValueError:
        raise HTTPException(status_code=404, detail="Agent not found")

    # LangChain Runnable vs LangGraph App 둘 다 .invoke 사용

    result = (
        agent.invoke({"input": body.input})
        if body.mode == "chain"
        else agent.invoke({"input": body.input})
    )

    return {"agent": agent_name, "input": body.input, "result": result}
