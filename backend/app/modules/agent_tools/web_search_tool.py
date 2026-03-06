import httpx

from app.modules.agent_tools.base_tool import BaseTool


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web using DuckDuckGo Instant Answer API."

    async def execute(self, input_data: dict) -> dict:
        query = input_data.get("query", "")
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
                "abstract": payload.get("AbstractText"),
                "heading": payload.get("Heading"),
                "related_topics": payload.get("RelatedTopics", [])[:5],
            }
