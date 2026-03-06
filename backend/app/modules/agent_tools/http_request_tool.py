import httpx

from app.modules.agent_tools.base_tool import BaseTool


class HttpRequestTool(BaseTool):
    name = "http_request"
    description = "Execute safe outbound HTTP requests for approved HTTPS endpoints."
    ALLOWED_METHODS = {"GET", "POST"}

    async def execute(self, input_data: dict) -> dict:
        method = str(input_data.get("method", "GET")).upper()
        url = str(input_data.get("url", ""))
        if method not in self.ALLOWED_METHODS:
            return {"error": "Method not allowed"}
        if not url.startswith("https://"):
            return {"error": "Only HTTPS URLs are allowed"}

        payload = input_data.get("json")
        headers = input_data.get("headers") or {}
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.request(method, url, json=payload, headers=headers)
            text = response.text
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": text[:3000],
            }
