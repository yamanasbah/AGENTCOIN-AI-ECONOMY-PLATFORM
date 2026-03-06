from fastapi import APIRouter

from app.endpoints import admin, health, marketplace, realtime, token
from app.modules.agent_runtime import router as runtime_router
from app.modules.agent_network import router as network_router
from app.modules.agents import router as agent_factory_router
from app.modules.agents import store_router as agent_store_router
from app.modules.analytics import router as analytics_router
from app.modules.api_keys import router as api_keys_router
from app.modules.auth import router as auth_router
from app.modules.notifications import router as notifications_router
from app.modules.wallet import router as wallet_router

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(api_keys_router, prefix="/api-keys", tags=["api-keys"])
api_router.include_router(agent_factory_router.router, prefix="/agents", tags=["agents"])
api_router.include_router(agent_store_router.router, prefix="/store", tags=["agent-store"])
api_router.include_router(wallet_router.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(marketplace.router, prefix="/marketplace", tags=["marketplace"])
api_router.include_router(token.router, prefix="/token", tags=["token"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(realtime.router, prefix="/realtime", tags=["realtime"])
api_router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(runtime_router.router, prefix="/runtime", tags=["runtime"])
api_router.include_router(network_router, tags=["agent-network"])
