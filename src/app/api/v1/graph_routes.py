# app/api/v1/graph_routes.py
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.graphs.base.base_graph import BaseGraph
from app.graphs.base.graph_registry import get_graph, list_graphs

router = APIRouter(prefix="/graph", tags=["graph"])

# 간단한 인스턴스 캐시 (그래프 빌드 비용 절약용)
_GRAPH_INSTANCE_CACHE: Dict[str, BaseGraph] = {}


class GraphRequest(BaseModel):
    graph_name: str
    # dict 기본값은 mutable 이라 Field(default_factory=dict) 권장
    input: Dict[str, Any] = Field(default_factory=dict)


@router.get("/list")
def list_available_graphs() -> Dict[str, Any]:
    """
    현재 애플리케이션에 등록된 그래프 목록을 반환.
    """
    return {"graphs": list(list_graphs().keys())}


@router.post("/run")
def run_graph(req: GraphRequest) -> Dict[str, Any]:
    """
    특정 그래프를 실행하는 엔드포인트.

    요청 예:
    {
      "graph_name": "echo",
      "input": { "text": "hello" }
    }
    """
    try:
        GraphCls = get_graph(req.graph_name)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Graph '{req.graph_name}' not found",
        )

    # 인스턴스 캐시 사용 (매번 build() 안 하도록)
    graph = _GRAPH_INSTANCE_CACHE.get(req.graph_name)
    if graph is None:
        try:
            graph = GraphCls()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to initialize graph '{req.graph_name}': {e}",
            )
        _GRAPH_INSTANCE_CACHE[req.graph_name] = graph

    try:
        # BaseGraph 인터페이스에 맞게 invoke 사용
        result = graph.invoke(req.input)
    except Exception as e:
        # LangGraph 내부 에러 등
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while running graph '{req.graph_name}': {e}",
        )

    return {
        "graph": req.graph_name,
        "result": result,
    }
