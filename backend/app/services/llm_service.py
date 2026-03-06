import json

import httpx

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model

    def generate(self, prompt: str, tools: list[dict]) -> dict:
        if not self.api_key:
            return {
                "content": "OPENAI_API_KEY is not configured. Unable to call external LLM.",
                "tool_call": None,
                "tokens_used": 0,
            }

        response = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an agent runtime orchestrator. "
                            "If you need a tool, return strict JSON with keys: "
                            "tool_name, tool_input, final_answer. "
                            "When no tool is needed, set tool_name to null and provide final_answer."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
                "tools": tools,
            },
            timeout=20.0,
        )
        response.raise_for_status()
        payload = response.json()

        message_content = payload["choices"][0]["message"].get("content") or "{}"
        parsed = json.loads(message_content)
        usage = payload.get("usage") or {}
        return {
            "content": parsed.get("final_answer") or "",
            "tool_call": (
                {
                    "name": parsed.get("tool_name"),
                    "input": parsed.get("tool_input") or {},
                }
                if parsed.get("tool_name")
                else None
            ),
            "tokens_used": usage.get("total_tokens", 0),
        }


llm_service = LLMService()
