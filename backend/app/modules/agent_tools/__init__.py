from app.modules.agent_tools.crypto_price_tool import CryptoPriceTool
from app.modules.agent_tools.http_request_tool import HttpRequestTool
from app.modules.agent_tools.tool_registry import TOOL_REGISTRY
from app.modules.agent_tools.web_search_tool import WebSearchTool

TOOL_REGISTRY.register_tool(CryptoPriceTool)
TOOL_REGISTRY.register_tool(HttpRequestTool)
TOOL_REGISTRY.register_tool(WebSearchTool)

__all__ = ["TOOL_REGISTRY", "CryptoPriceTool", "HttpRequestTool", "WebSearchTool"]
