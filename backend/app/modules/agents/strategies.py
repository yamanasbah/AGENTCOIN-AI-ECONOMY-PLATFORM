from abc import ABC, abstractmethod

from app.modules.agents.models import AgentStrategyType, ManagedAgent


class StrategyBase(ABC):
    def __init__(self, agent: ManagedAgent):
        self.agent = agent

    @abstractmethod
    def execute(self) -> float:
        pass

    @abstractmethod
    def risk_check(self) -> bool:
        pass

    @abstractmethod
    def generate_signal(self) -> float:
        pass


class BaseSimpleStrategy(StrategyBase):
    multiplier = 0.01

    def generate_signal(self) -> float:
        return float(self.agent.initial_capital) * self.multiplier

    def risk_check(self) -> bool:
        return float(self.agent.initial_capital) > 0 and self.agent.status.value == "running"

    def execute(self) -> float:
        if not self.risk_check():
            return 0.0
        return max(self.generate_signal(), 0.0)


class GridTradingStrategy(BaseSimpleStrategy):
    multiplier = 0.012


class MomentumStrategy(BaseSimpleStrategy):
    multiplier = 0.018


class ArbitrageStrategy(BaseSimpleStrategy):
    multiplier = 0.01


class AITraderStrategy(BaseSimpleStrategy):
    multiplier = 0.02


def get_strategy(agent: ManagedAgent) -> StrategyBase:
    mapping = {
        AgentStrategyType.grid_trading: GridTradingStrategy,
        AgentStrategyType.momentum: MomentumStrategy,
        AgentStrategyType.arbitrage: ArbitrageStrategy,
        AgentStrategyType.ai_trader: AITraderStrategy,
    }
    return mapping[agent.strategy_type](agent)
