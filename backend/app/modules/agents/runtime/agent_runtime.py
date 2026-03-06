import json
import time
from decimal import Decimal

from app.modules.agents.models import ManagedAgent
from app.modules.agents.tools import TOOL_REGISTRY
from app.services.llm_service import llm_service


class AgentRuntime:
    DEFAULT_TOOLS = ["web_search", "crypto_price", "http_request", "memory_store"]

    @classmethod
    def execute(cls, agent: ManagedAgent, user_input: str) -> dict:
        started_at = time.perf_counter()
        toolset = cls._build_toolset(agent.capabilities or {})

        tool_specs = [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "additionalProperties": True,
                    },
                },
            }
            for name, tool in toolset.items()
        ]

        prompt = cls._build_prompt(agent.system_prompt, agent.capabilities or {}, user_input)
        llm_result = llm_service.generate(prompt, tool_specs)

        final_output = llm_result.get("content", "")
        invoked_tool = llm_result.get("tool_call")
        if invoked_tool:
            tool_name = invoked_tool.get("name")
            tool_input = invoked_tool.get("input") or {}
            tool = toolset.get(tool_name)
            tool_result = tool.run(tool_input) if tool else {"error": f"Unknown tool: {tool_name}"}
            final_output = cls._build_tool_augmented_output(final_output, tool_name, tool_result)

        execution_time = time.perf_counter() - started_at
        return {
            "input": user_input,
            "output": final_output,
            "tokens_used": int(llm_result.get("tokens_used", 0)),
            "execution_time": float(round(execution_time, 6)),
            "status": "success",
        }

    @classmethod
    def _build_toolset(cls, capabilities: dict) -> dict:
        enabled_tools = capabilities.get("tools") or cls.DEFAULT_TOOLS
        toolset = {}
        for tool_name in enabled_tools:
            tool_class = TOOL_REGISTRY.get(tool_name)
            if tool_class:
                toolset[tool_name] = tool_class()
        return toolset

    @staticmethod
    def _build_prompt(system_prompt: str, capabilities: dict, user_input: str) -> str:
        return (
            f"System Prompt:\n{system_prompt}\n\n"
            f"Capabilities:\n{json.dumps(capabilities)}\n\n"
            f"User Input:\n{user_input}"
        )

    @staticmethod
    def _build_tool_augmented_output(final_output: str, tool_name: str, tool_result: dict) -> str:
        return (
            f"{final_output}\n\n"
            f"Tool used: {tool_name}\n"
            f"Tool result: {json.dumps(tool_result)}"
        ).strip()

    @staticmethod
    def to_decimal_tokens(tokens_used: int) -> Decimal:
        return Decimal(tokens_used)
