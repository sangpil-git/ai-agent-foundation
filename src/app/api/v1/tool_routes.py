# app/api/v1/tool_routes.py
from fastapi import APIRouter
from app.tools import tool_registry

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("/list")
def list_tools():
    return {"tools": list(tool_registry.list_active_tools().keys())}
