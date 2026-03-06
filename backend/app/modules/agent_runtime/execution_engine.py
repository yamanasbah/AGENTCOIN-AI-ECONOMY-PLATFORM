from __future__ import annotations

import asyncio
import json
import re
import time
from uuid import UUID

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.modules.agents.models import AgentLog, ManagedAgent
from app.modules.agent_runtime.memory_store import AgentMemoryStore
from app.modules.agent_runtime.tool_registry import TOOL_REGISTRY


class ExecutionEngine:
    def __init__(self, db: Session, memory_store: AgentMemoryStore) -> None:
        self.db = db
        self.memory_store = memory_store

    def run(self, agent: ManagedAgent, user_input: str) -> dict:
        started = time.perf_counter()
        prompt = self.build_prompt(agent)
        memory = self.inject_memory(agent.id)
        llm_output = self.execute_with_llm(prompt, user_input, memory, self._agent_tools(agent))
        tool_output = self.call_tools_if_needed(llm_output)
        elapsed = time.perf_counter() - started
        return self.save_logs(agent.id, user_input, llm_output, tool_output, elapsed)

    def load_agent(self, agent_id: UUID) -> ManagedAgent:
        agent = self.db.query(ManagedAgent).filter(ManagedAgent.id == agent_id).first()
        if not agent:
            raise ValueError("Agent not found")
        return agent

    def build_prompt(self, agent: ManagedAgent) -> str:
        tool_lines = "\n".join(f"- {tool['name']}: {tool['description']}" for tool in self._agent_tools(agent))
        return (
            f"{agent.system_prompt}\n\n"
            "You are an execution agent in AgentCoin AI Economy.\n"
            "Available tools:\n"
            f"{tool_lines}\n"
            "If you need a tool, include a line exactly like: TOOL_CALL <tool_name> <json_payload>."
        )

    def inject_memory(self, agent_id: UUID) -> list[dict[str, str]]:
        entries = self.memory_store.load_memory(agent_id)
        return [{"key": item.memory_key, "value": item.memory_value} for item in entries]

    def execute_with_llm(self, system_prompt: str, user_input: str, memory: list[dict], tools: list[dict]) -> dict:
        provider = settings.llm_provider.lower()
        if provider == "openai":
            return asyncio.run(self._openai_completion(system_prompt, user_input, memory, tools))
        return {
            "result": f"[generic:{provider}] {user_input}",
            "tokens_used": 0,
            "raw": "Generic provider fallback response.",
        }

    def call_tools_if_needed(self, llm_output: dict) -> dict | None:
        raw_text = str(llm_output.get("raw") or llm_output.get("result") or "")
        match = re.search(r"TOOL_CALL\s+(\w+)\s+(\{.*\})", raw_text, re.DOTALL)
        if not match:
            return None

        tool_name = match.group(1)
        payload_str = match.group(2)
        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError:
            return {"error": "invalid tool payload", "tool": tool_name}

        tool = TOOL_REGISTRY.get_tool(tool_name)
        if not tool:
            return {"error": "tool not found", "tool": tool_name}
        return asyncio.run(tool.execute(payload))

    def save_logs(self, agent_id: UUID, user_input: str, llm_output: dict, tool_output: dict | None, execution_time: float) -> dict:
        result_text = str(llm_output.get("result") or "")
        if tool_output:
            result_text = f"{result_text}\n\nTool Output:\n{json.dumps(tool_output, ensure_ascii=False)}"

        log = AgentLog(
            agent_id=agent_id,
            execution_message=result_text,
            tokens_consumed=0,
            input_payload=user_input,
            output_payload=result_text,
            input_text=user_input,
            output_text=result_text,
            execution_cost=0,
            tokens_used=llm_output.get("tokens_used", 0),
            execution_time=execution_time,
            status="success",
        )
        self.db.add(log)

        self.memory_store.save_memory(agent_id, "last_user_input", user_input)
        self.memory_store.save_memory(agent_id, "last_agent_output", result_text)

        return {
            "result": result_text,
            "tokens_used": int(llm_output.get("tokens_used", 0)),
            "execution_time": execution_time,
            "log": log,
        }

    def _agent_tools(self, agent: ManagedAgent) -> list[dict[str, str]]:
        configured = (agent.capabilities or {}).get("tools") or []
        all_tools = {item["name"]: item for item in TOOL_REGISTRY.list_tools()}
        if not configured:
            return list(all_tools.values())
        return [all_tools[name] for name in configured if name in all_tools]

    async def _openai_completion(self, system_prompt: str, user_input: str, memory: list[dict], tools: list[dict]) -> dict:
        api_key = settings.llm_api_key or settings.openai_api_key
        if not api_key:
            return {"result": "LLM API key is not configured.", "tokens_used": 0, "raw": ""}

        url = f"{settings.llm_api_base.rstrip('/')}/chat/completions"
        messages = [{"role": "system", "content": system_prompt}]
        for item in memory:
            messages.append({"role": "system", "content": f"Memory[{item['key']}]: {item['value']}"})
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
                url,
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": settings.llm_model or settings.openai_model,
                    "messages": messages,
                    "tools": tool_specs,
                    "temperature": 0.2,
                },
            )
            response.raise_for_status()
            payload = response.json()

        message = payload["choices"][0]["message"]
        content = message.get("content") or ""
        usage = payload.get("usage") or {}

        return {
            "result": content,
            "tokens_used": int(usage.get("total_tokens", 0)),
            "raw": content,
        }
