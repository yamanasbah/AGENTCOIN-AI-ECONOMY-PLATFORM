from fastapi import APIRouter

from app.endpoints import admin, agents, health, marketplace, realtime, token

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(marketplace.router, prefix="/marketplace", tags=["marketplace"])
api_router.include_router(token.router, prefix="/token", tags=["token"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(realtime.router, prefix="/realtime", tags=["realtime"])
