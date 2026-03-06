import httpx

from app.modules.agents.tools.base import AgentTool


class HttpRequestTool(AgentTool):
    name = "http_request"
    description = "Performs outbound HTTP requests for GET/POST/PUT/DELETE."

    def run(self, input: dict) -> dict:
        input = input or {}
        url = input.get("url")
        method = (input.get("method") or "GET").upper()
        if not url:
            return {"error": "Missing url"}

        headers = input.get("headers") or {}
        params = input.get("params") or {}
        json_body = input.get("json")

        try:
            response = httpx.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=10.0,
            )
            content_type = response.headers.get("content-type", "")
            body: dict | str
            if "application/json" in content_type:
                body = response.json()
            else:
                body = response.text[:2000]
            return {"status_code": response.status_code, "headers": dict(response.headers), "body": body}
        except Exception as exc:
            return {"error": str(exc), "url": url, "method": method}
