from fastapi import APIRouter

from app.endpoints import admin, health, marketplace, realtime, token
from app.modules.agents import router as agent_factory_router
from app.modules.wallet import router as wallet_router
from app.modules.agent_runtime import router as runtime_router

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(agent_factory_router.router, prefix="/agents", tags=["agents"])
api_router.include_router(wallet_router.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(marketplace.router, prefix="/marketplace", tags=["marketplace"])
api_router.include_router(token.router, prefix="/token", tags=["token"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(realtime.router, prefix="/realtime", tags=["realtime"])

api_router.include_router(runtime_router.router, prefix="/runtime", tags=["runtime"])
