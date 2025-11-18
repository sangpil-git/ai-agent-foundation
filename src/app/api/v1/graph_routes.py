# app/api/v1/graph_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from app.graphs.base.graph_registry import get_graph, list_graphs

router = APIRouter(prefix="/graph", tags=["graph"])


class GraphRequest(BaseModel):
    graph_name: str
    input: Dict[str, Any] = {}


@router.get("/list")
def list_available_graphs():
    return {"graphs": list(list_graphs().keys())}


@router.post("/run")
def run_graph(req: GraphRequest):
    try:
        GraphCls = get_graph(req.graph_name)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Graph '{req.graph_name}' not found")

    graph = GraphCls()
    result = graph.run(req.input)
    return {"graph": req.graph_name, "result": result}
