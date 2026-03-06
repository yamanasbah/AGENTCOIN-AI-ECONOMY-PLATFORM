import json

import httpx

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model

    async def generate_response(self, system_prompt: str, user_input: str, tools: list, memory: list) -> dict:
        if not self.api_key:
            return {"result": "OPENAI_API_KEY is not configured.", "tokens_used": 0}

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(memory)
        messages.append({"role": "user", "content": user_input})

        tool_specs = [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": {"type": "object", "additionalProperties": True},
                },
            }
            for tool in tools
        ]

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": messages,
                    "tools": tool_specs,
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"},
                },
            )
            response.raise_for_status()
            payload = response.json()

        message = payload["choices"][0]["message"]
        content = message.get("content") or "{}"
        try:
            parsed = json.loads(content)
            result = parsed.get("final_answer") or content
        except json.JSONDecodeError:
            result = content

        usage = payload.get("usage") or {}
        return {"result": result, "tokens_used": int(usage.get("total_tokens", 0))}
