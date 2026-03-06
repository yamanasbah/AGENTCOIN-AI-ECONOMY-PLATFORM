from __future__ import annotations

import re
from abc import ABC, abstractmethod

import httpx


class RuntimeTool(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    async def execute(self, input_data: dict) -> dict:
        raise NotImplementedError


class SearchWebTool(RuntimeTool):
    name = "search_web_tool"
    description = "Search the web with DuckDuckGo instant answers. Input: {query}."

    async def execute(self, input_data: dict) -> dict:
        query = str(input_data.get("query", "")).strip()
        if not query:
            return {"error": "query is required"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_redirect": 1, "no_html": 1},
            )
            response.raise_for_status()
            payload = response.json()
            return {
                "heading": payload.get("Heading"),
                "abstract": payload.get("AbstractText"),
                "related_topics": payload.get("RelatedTopics", [])[:5],
            }


class HttpRequestTool(RuntimeTool):
    name = "http_request_tool"
    description = "Execute safe HTTPS GET/POST requests. Input: {url, method, json?}."
    ALLOWED_METHODS = {"GET", "POST"}

    async def execute(self, input_data: dict) -> dict:
        method = str(input_data.get("method", "GET")).upper()
        url = str(input_data.get("url", ""))
        if method not in self.ALLOWED_METHODS:
            return {"error": "method not allowed"}
        if not url.startswith("https://"):
            return {"error": "only https URLs are allowed"}

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.request(method, url, json=input_data.get("json"), headers=input_data.get("headers") or {})
            return {
                "status_code": response.status_code,
                "body": response.text[:3000],
                "headers": dict(response.headers),
            }


class CryptoPriceTool(RuntimeTool):
    name = "crypto_price_tool"
    description = "Get live token prices from CoinGecko. Input: {coin_id, vs_currency}."

    async def execute(self, input_data: dict) -> dict:
        coin_id = input_data.get("coin_id", "bitcoin")
        vs_currency = input_data.get("vs_currency", "usd")
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": coin_id, "vs_currencies": vs_currency},
            )
            response.raise_for_status()
            return response.json()


class SummarizeTextTool(RuntimeTool):
    name = "summarize_text_tool"
    description = "Summarize text locally. Input: {text}."

    async def execute(self, input_data: dict) -> dict:
        text = re.sub(r"\s+", " ", str(input_data.get("text", "")).strip())
        if not text:
            return {"error": "text is required"}
        sentences = re.split(r"(?<=[.!?])\s+", text)
        summary = " ".join(sentences[:2])[:400]
        return {"summary": summary or text[:400]}


class ToolRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, type[RuntimeTool]] = {}

    def register_tool(self, tool_cls: type[RuntimeTool]) -> None:
        self._registry[tool_cls.name] = tool_cls

    def get_tool(self, name: str) -> RuntimeTool | None:
        tool_cls = self._registry.get(name)
        return tool_cls() if tool_cls else None

    def list_tools(self) -> list[dict[str, str]]:
        return [
            {"name": tool_name, "description": self._registry[tool_name].description}
            for tool_name in sorted(self._registry.keys())
        ]


TOOL_REGISTRY = ToolRegistry()
TOOL_REGISTRY.register_tool(SearchWebTool)
TOOL_REGISTRY.register_tool(HttpRequestTool)
TOOL_REGISTRY.register_tool(CryptoPriceTool)
TOOL_REGISTRY.register_tool(SummarizeTextTool)
