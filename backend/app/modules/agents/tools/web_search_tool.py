from app.modules.agents.tools.base import AgentTool


class WebSearchTool(AgentTool):
    name = "web_search"
    description = "Searches the web and returns lightweight results."

    def run(self, input: dict) -> dict:
        query = (input or {}).get("query")
        if not query:
            return {"error": "Missing query"}

        # Placeholder implementation to keep runtime offline-safe.
        return {
            "query": query,
            "results": [
                {
                    "title": f"Search result for: {query}",
                    "url": "https://example.com/search",
                    "snippet": "Web search provider not configured; returned simulated result.",
                }
            ],
        }
