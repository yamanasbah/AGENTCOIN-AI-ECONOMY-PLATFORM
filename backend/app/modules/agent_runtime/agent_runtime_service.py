from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.agent_runtime.agent_executor import AgentExecutor
from app.modules.agent_runtime.llm_service import LLMService
from app.modules.agent_tools import TOOL_REGISTRY
from app.modules.agents.models import AgentLog, AgentStatus, ManagedAgent
from app.modules.agents.services.agent_memory_service import AgentMemoryService
from app.modules.wallet.models import TransactionType, WalletOwnerType
from app.modules.wallet.service import WalletService


class AgentRuntimeService:
    EXECUTION_COST = 1.0

    def __init__(self, db: Session) -> None:
        self.db = db
        self.executor = AgentExecutor(LLMService())

    def run_agent(self, agent_id: UUID, input_text: str, caller_user_id: int | None = None) -> AgentLog:
        agent = self.db.query(ManagedAgent).filter(ManagedAgent.id == agent_id).first()
        if not agent:
            raise ValueError("Agent not found")
        if agent.status == AgentStatus.paused:
            raise ValueError("Agent is not active")

        payer_id = caller_user_id if caller_user_id is not None else agent.owner_user_id
        payer_wallet = WalletService.get_or_create_wallet(self.db, WalletOwnerType.user, str(payer_id))
        agent_wallet = WalletService.get_wallet_by_id(self.db, agent.wallet_id)
        WalletService.transfer_tokens(
            self.db,
            from_wallet=payer_wallet,
            to_wallet=agent_wallet,
            amount=self.EXECUTION_COST,
            tx_type=TransactionType.execution,
        )

        configured_tools = (agent.capabilities or {}).get("tools") or []
        tools = []
        for tool_name in configured_tools:
            tool = TOOL_REGISTRY.get_tool(tool_name)
            if tool:
                tools.append({"name": tool.name, "description": tool.description})

        memory_entries = AgentMemoryService.get_recent_memory(self.db, agent.id, limit=10)
        serialized_memory = self.executor.serialize_memory(memory_entries)
        system_prompt = self.executor.build_system_prompt(agent.system_prompt, tools)

        agent.status = AgentStatus.running
        llm_result = self.executor.execute(system_prompt, input_text, tools, serialized_memory)
        agent.status = AgentStatus.idle

        output_text = llm_result.get("result", "")
        tokens_used = llm_result.get("tokens_used", 0)

        AgentMemoryService.add_memory(self.db, agent.id, "user", input_text)
        AgentMemoryService.add_memory(self.db, agent.id, "assistant", output_text)

        log = AgentLog(
            agent_id=agent.id,
            execution_message=output_text,
            tokens_consumed=Decimal(str(self.EXECUTION_COST)),
            input_payload=input_text,
            output_payload=output_text,
            input_text=input_text,
            output_text=output_text,
            execution_cost=Decimal(str(self.EXECUTION_COST)),
            tokens_used=Decimal(str(tokens_used)),
            status="success",
        )
        self.db.add(log)
        return log
