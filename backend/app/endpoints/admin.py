from fastapi import APIRouter

router = APIRouter()

SAFE_MODE = {"enabled": False}
RISK_LIMITS = {"max_global_drawdown": 25}


@router.get("/analytics")
def admin_analytics():
    return {
        "token_usage": {"staked": 125000, "burned": 3500},
        "revenue": {"mrr_token": 5800, "commission_token": 2100},
        "agent_growth": {"total_agents": 842, "active_agents": 517},
    }


@router.post("/safe-mode")
def set_safe_mode(enabled: bool):
    SAFE_MODE["enabled"] = enabled
    return SAFE_MODE


@router.post("/risk-limits")
def update_global_risk_limits(max_global_drawdown: int):
    RISK_LIMITS["max_global_drawdown"] = max_global_drawdown
    return RISK_LIMITS
