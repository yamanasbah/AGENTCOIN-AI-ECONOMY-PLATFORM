from collections import defaultdict

from app.modules.agents.tools.base import AgentTool


class MemoryStoreTool(AgentTool):
    name = "memory_store"
    description = "Stores and reads in-memory key/value pairs for an agent runtime session."

    def __init__(self) -> None:
        self._store = defaultdict(dict)

    def run(self, input: dict) -> dict:
        input = input or {}
        namespace = input.get("namespace") or "default"
        action = (input.get("action") or "get").lower()
        key = input.get("key")

        if action == "set":
            if key is None:
                return {"error": "Missing key for set"}
            self._store[namespace][str(key)] = input.get("value")
            return {"ok": True, "namespace": namespace, "key": str(key)}

        if action == "get":
            if key is None:
                return {"error": "Missing key for get"}
            return {"namespace": namespace, "key": str(key), "value": self._store[namespace].get(str(key))}

        if action == "list":
            return {"namespace": namespace, "values": self._store[namespace]}

        return {"error": f"Unsupported action: {action}"}
