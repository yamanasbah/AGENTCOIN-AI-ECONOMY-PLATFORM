from app.modules.agents.tools.base import AgentTool
from app.modules.agents.tools.crypto_price_tool import CryptoPriceTool
from app.modules.agents.tools.http_request_tool import HttpRequestTool
from app.modules.agents.tools.memory_store_tool import MemoryStoreTool
from app.modules.agents.tools.web_search_tool import WebSearchTool

TOOL_REGISTRY: dict[str, type[AgentTool]] = {
    WebSearchTool.name: WebSearchTool,
    CryptoPriceTool.name: CryptoPriceTool,
    HttpRequestTool.name: HttpRequestTool,
    MemoryStoreTool.name: MemoryStoreTool,
}

__all__ = [
    "AgentTool",
    "WebSearchTool",
    "CryptoPriceTool",
    "HttpRequestTool",
    "MemoryStoreTool",
    "TOOL_REGISTRY",
]
