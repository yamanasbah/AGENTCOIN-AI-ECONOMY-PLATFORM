from abc import ABC, abstractmethod

from app.modules.agents.models import AgentType, ManagedAgent


class StrategyBase(ABC):
    def __init__(self, agent: ManagedAgent):
        self.agent = agent

    @abstractmethod
    def execute(self) -> float:
        pass


class BaseSimpleStrategy(StrategyBase):
    multiplier = 1.0

    def execute(self) -> float:
        return self.multiplier


class MarketingStrategy(BaseSimpleStrategy):
    multiplier = 1.1


class TradingStrategy(BaseSimpleStrategy):
    multiplier = 1.4


class ResearchStrategy(BaseSimpleStrategy):
    multiplier = 1.0


class AutomationStrategy(BaseSimpleStrategy):
    multiplier = 1.2


class CustomStrategy(BaseSimpleStrategy):
    multiplier = 1.0


def get_strategy(agent: ManagedAgent) -> StrategyBase:
    mapping = {
        AgentType.marketing_agent: MarketingStrategy,
        AgentType.trading_agent: TradingStrategy,
        AgentType.research_agent: ResearchStrategy,
        AgentType.automation_agent: AutomationStrategy,
        AgentType.custom_agent: CustomStrategy,
    }
    return mapping[agent.agent_type](agent)
