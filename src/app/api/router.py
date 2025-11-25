# app/api/router.py
from fastapi import APIRouter

from app.api.v1.chain_routes import router as chain_router
from app.api.v1.graph_routes import router as graph_router
from app.api.v1.tool_routes import router as tool_router
from app.api.v1.health_routes import router as health_router


api_router = APIRouter(prefix="/api")

# v1 네임스페이스
api_router.include_router(chain_router, prefix="/v1") 
api_router.include_router(graph_router, prefix="/v1")
api_router.include_router(tool_router, prefix="/v1")
api_router.include_router(health_router, prefix="/v1")
