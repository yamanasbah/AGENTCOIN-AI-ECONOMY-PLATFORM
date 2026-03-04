from fastapi import APIRouter

from app.services.token_service import TOKEN_SERVICE

router = APIRouter()


@router.post("/stake")
def stake_tokens(amount: float, wallet: str):
    return TOKEN_SERVICE.stake_for_agent_activation(wallet=wallet, amount=amount)


@router.get("/wallet/connect-placeholder")
def wallet_connect_placeholder():
    return {"status": "placeholder", "message": "Integrate RainbowKit/Web3Auth in frontend"}
