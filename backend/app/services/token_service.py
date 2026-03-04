from dataclasses import dataclass

from app.core.config import settings


@dataclass
class TokenOperationResult:
    success: bool
    message: str
    tx_hash: str | None = None


class TokenService:
    """ERC20-ready placeholder service with staking + burn hooks."""

    def stake_for_agent_activation(self, wallet: str, amount: float) -> TokenOperationResult:
        if amount < settings.token_min_stake:
            return TokenOperationResult(False, f"Minimum stake is {settings.token_min_stake} {settings.token_symbol}")
        return TokenOperationResult(True, "Stake accepted (off-chain placeholder)", tx_hash="0xstakeplaceholder")

    def burn_on_agent_creation(self, wallet: str) -> TokenOperationResult:
        return TokenOperationResult(
            True,
            f"Burned {settings.token_agent_creation_burn} {settings.token_symbol} for agent creation",
            tx_hash="0xburnplaceholder",
        )

    def distribute_commission(self, wallet: str, amount: float) -> TokenOperationResult:
        return TokenOperationResult(True, f"Distributed {amount} {settings.token_symbol}", tx_hash="0xcommissionplaceholder")


TOKEN_SERVICE = TokenService()
