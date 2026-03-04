from fastapi import APIRouter

router = APIRouter()


@router.get("/channels")
def channels():
    return [
        "live_balance_updates",
        "live_trade_feed",
        "safe_mode_alerts",
        "token_staking_updates",
    ]
