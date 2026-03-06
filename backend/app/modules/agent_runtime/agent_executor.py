import asyncio
import json

from app.modules.agent_runtime.llm_service import LLMService


class AgentExecutor:
    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    def execute(self, system_prompt: str, user_input: str, tools: list[dict], memory: list[dict]) -> dict:
        return asyncio.run(
            self.llm_service.generate_response(
                system_prompt=system_prompt,
                user_input=user_input,
                tools=tools,
                memory=memory,
            )
        )

    @staticmethod
    def build_system_prompt(base_prompt: str, tools: list[dict]) -> str:
        tool_lines = "\n".join(f"- {tool['name']}: {tool['description']}" for tool in tools)
        return (
            f"{base_prompt}\n\n"
            "You are an AI execution agent in a multi-tenant economy.\n"
            "You may use tools by reasoning over available capabilities.\n"
            f"Available tools:\n{tool_lines}\n"
            "Respond in JSON with key final_answer."
        )

    @staticmethod
    def serialize_memory(memory_entries: list) -> list[dict]:
        return [{"role": entry.role, "content": entry.content} for entry in memory_entries]

    @staticmethod
    def safe_json(value: dict) -> str:
        return json.dumps(value, ensure_ascii=False)
