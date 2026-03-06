from abc import ABC, abstractmethod


class AgentTool(ABC):
    name: str = "tool"
    description: str = ""

    @abstractmethod
    def run(self, input: dict) -> dict:
        raise NotImplementedError
