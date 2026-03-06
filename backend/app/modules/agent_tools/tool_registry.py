from app.modules.agent_tools.base_tool import BaseTool


class ToolRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, type[BaseTool]] = {}

    def register_tool(self, tool_cls: type[BaseTool]) -> None:
        self._registry[tool_cls.name] = tool_cls

    def get_tool(self, name: str) -> BaseTool | None:
        tool_cls = self._registry.get(name)
        return tool_cls() if tool_cls else None

    def list_tools(self) -> list[str]:
        return sorted(self._registry.keys())


TOOL_REGISTRY = ToolRegistry()
