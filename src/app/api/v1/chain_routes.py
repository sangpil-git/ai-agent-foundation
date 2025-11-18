# app/api/v1/chain_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

from app.chains.base.chain_registry import get_chain, list_chains
from app.core.logging import logger
from app.utils.move.response_builder import error_response, success_response

router = APIRouter(prefix="/chain", tags=["chain"])


class ChainRequest(BaseModel):
    chain_name: str                                     # 예: "summarize"
    model_name: Optional[str] = None                    # 예: "gpt-4.1-mini" (선택)
    input: Dict[str, Any] = Field(default_factory=dict) # 체인에 넘길 실제 input


@router.get("/list")
def list_available_chains():
    """
    등록된 체인 목록 조회
    """
    return {"chains": list(list_chains().keys())}


@router.post("/run")
def run_chain(req: ChainRequest):
    """
    특정 체인을 실행.
    body 예:
    {
      "chain_name": "summarize",
      "model_name": "gpt-4.1-mini" (선택),
      "input": { "text": "요약할 텍스트..." }
    }
    """
    try:
        ChainCls = get_chain(req.chain_name)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message=f"Chain '{req.chain_name}' not found",
                code="CHAIN_NOT_FOUND",
            )
        )

    try:
        chain = ChainCls(model_name=req.model_name)
        chain_result = chain.invoke(req.input)
    except Exception as e:
        logger.exception("Chain execution error", extra={
            "chain_name": req.chain_name,
            "model_name": req.model_name,
        })
        raise HTTPException(
            status_code=400,
            detail=error_response(
                message=str(e),
                code="CHAIN_EXECUTION_ERROR",
            )
        )

    data = {
        "chain": req.chain_name,
        "model": getattr(chain, "model_name", None),
        **chain_result,
    }

    return success_response(data)
