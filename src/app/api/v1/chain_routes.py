# app/api/v1/chain_routes.py
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.chains.base.chain_registry import get_chain, list_chains
from app.core.logging.logger import get_logger
from app.utils.response import success_response

router = APIRouter(prefix="/chain", tags=["chain"])
logger = get_logger("chain")


class ChainRequest(BaseModel):
    chain_name: str                                     # 예: "summarize"
    model_name: Optional[str] = None                    # 예: "gpt-4.1-mini" (선택)
    input: Dict[str, Any] = Field(default_factory=dict) # 체인에 넘길 실제 input
    options: dict = Field(default_factory=dict)


@router.get("/list")
def list_available_chains() -> Dict[str, Any]:
    """
    등록된 체인 목록 조회
    """
    return {"chains": list(list_chains().keys())}


@router.post("/run")
def run_chain(req: ChainRequest):
    """
    body 예:
    {
      "chain_name": "summarize",
      "model_name": "gpt-4.1-mini",   # 선택
      "input": { "text": "요약할 텍스트..." }
    }
    """
    # 1) 체인 조회
    try:
        ChainCls = get_chain(req.chain_name)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chain '{req.chain_name}' not found",
        )

    # 2) 체인 인스턴스 생성
    try:
        chain = ChainCls(
            model_name=req.model_name,
            **(req.options or {}),
        )
    except Exception:
        logger.exception(
            "Chain initialization error",
            extra={"chain_name": req.chain_name, "model_name": req.model_name},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="체인 초기화 중 오류가 발생했습니다.",
        )

    # 3) 체인 실행
    try:
        # req.input이 None일 수 있으면 {} 기본값
        input_payload = req.input or {}
        chain_result = chain.invoke(input_payload)
    except ValueError as e:
        # BaseChain.validate_input 등에서 발생하는 입력 검증 오류
        logger.warning(
            "Chain validation error",
            extra={
                "chain_name": req.chain_name,
                "model_name": req.model_name,
                "input": req.input,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        logger.exception(
            "Chain execution error",
            extra={
                "chain_name": req.chain_name,
                "model_name": req.model_name,
                "input": req.input,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e) ,
        )

    # 4) 응답 래핑 (구조 고정)
    data: Dict[str, Any] = {
        "chain": req.chain_name,
        "model": getattr(chain, "model_name", None),
        "result": chain_result,   # 결과는 항상 result 안에
    }

    return success_response(data)

