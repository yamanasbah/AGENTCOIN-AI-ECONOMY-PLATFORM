from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.agent_network.models import AgentCapability, AgentReputation, AgentSchedule, AgentWorkflow, WorkflowStep
from app.modules.agents.models import AgentTask, ManagedAgent
from app.modules.wallet.models import TransactionType, WalletOwnerType
from app.modules.wallet.service import WalletService


class AgentDiscoveryService:
    @staticmethod
    def find_agents_by_capability(db: Session, capability: str) -> list[tuple[ManagedAgent, AgentCapability]]:
        return (
            db.query(ManagedAgent, AgentCapability)
            .join(AgentCapability, AgentCapability.agent_id == ManagedAgent.id)
            .filter(AgentCapability.capability_name == capability, ManagedAgent.is_published.is_(True))
            .all()
        )

    @staticmethod
    def rank_agents_by_rating(agent_pairs: list[tuple[ManagedAgent, AgentCapability]]) -> list[tuple[ManagedAgent, AgentCapability]]:
        return sorted(agent_pairs, key=lambda row: float(row[0].average_rating or 0), reverse=True)

    @staticmethod
    def rank_agents_by_cost(agent_pairs: list[tuple[ManagedAgent, AgentCapability]]) -> list[tuple[ManagedAgent, AgentCapability]]:
        return sorted(agent_pairs, key=lambda row: float(row[0].price_per_run or 0))


class AgentNetworkService:
    @staticmethod
    def create_capability(db: Session, agent_id: UUID, capability_name: str, description: str | None) -> AgentCapability:
        capability = AgentCapability(agent_id=agent_id, capability_name=capability_name, description=description)
        db.add(capability)
        return capability

    @staticmethod
    def list_capabilities(db: Session) -> list[AgentCapability]:
        return db.query(AgentCapability).order_by(AgentCapability.capability_name.asc()).all()

    @staticmethod
    def discover_agents(db: Session, capability: str, rank_by: str = "rating") -> list[dict]:
        candidates = AgentDiscoveryService.find_agents_by_capability(db, capability)
        if rank_by == "cost":
            candidates = AgentDiscoveryService.rank_agents_by_cost(candidates)
        else:
            candidates = AgentDiscoveryService.rank_agents_by_rating(candidates)

        results = []
        for agent, cap in candidates:
            rep = db.query(AgentReputation).filter(AgentReputation.agent_id == agent.id).first()
            results.append(
                {
                    "agent_id": agent.id,
                    "name": agent.name,
                    "capability_name": cap.capability_name,
                    "rating": float(agent.average_rating or 0),
                    "cost": float(agent.price_per_run or 0),
                    "reputation_score": float(rep.score if rep else 0),
                }
            )
        return results

    @staticmethod
    def create_task_contract(
        db: Session,
        requester_agent_id: UUID,
        worker_agent_id: UUID,
        task_description: str,
        payment_amount: float,
        current_user_id: int,
    ) -> AgentTask:
        requester = db.query(ManagedAgent).filter(ManagedAgent.id == requester_agent_id).first()
        worker = db.query(ManagedAgent).filter(ManagedAgent.id == worker_agent_id).first()
        if not requester or not worker:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
        if requester.owner_user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create contracts for another owner's agent")

        requester_wallet = WalletService.get_wallet(db, WalletOwnerType.agent, str(requester.id))
        if not requester_wallet:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Requester agent wallet not found")

        WalletService.lock_tokens(db, requester_wallet, payment_amount)

        contract = AgentTask(
            agent_id=worker.id,
            task_type="agent_contract",
            payload={"input": task_description},
            status="created",
            requester_agent_id=requester.id,
            worker_agent_id=worker.id,
            task_description=task_description,
            payment_amount=payment_amount,
        )
        db.add(contract)
        AgentNetworkService.update_reputation(db, worker.id)
        return contract

    @staticmethod
    def update_contract_status(db: Session, contract_id: int, status_value: str, current_user_id: int) -> AgentTask:
        valid_statuses = {"created", "accepted", "running", "completed", "failed"}
        if status_value not in valid_statuses:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")

        contract = db.query(AgentTask).filter(AgentTask.id == contract_id).first()
        if not contract or not contract.requester_agent_id or not contract.worker_agent_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")

        requester = db.query(ManagedAgent).filter(ManagedAgent.id == contract.requester_agent_id).first()
        worker = db.query(ManagedAgent).filter(ManagedAgent.id == contract.worker_agent_id).first()
        if not requester or not worker:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

        if current_user_id not in {requester.owner_user_id, worker.owner_user_id}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this contract")

        contract.status = status_value
        if status_value in {"completed", "failed"}:
            contract.completed_at = datetime.utcnow()
            contract.finished_at = contract.completed_at

        if status_value == "completed":
            requester_wallet = WalletService.get_wallet(db, WalletOwnerType.agent, str(requester.id))
            worker_wallet = WalletService.get_wallet(db, WalletOwnerType.agent, str(worker.id))
            if not requester_wallet or not worker_wallet:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agent wallet not found")

            WalletService.unlock_tokens(db, requester_wallet, float(contract.payment_amount))
            WalletService.transfer_tokens(
                db,
                requester_wallet,
                worker_wallet,
                float(contract.payment_amount),
                tx_type=TransactionType.execution,
            )
            AgentNetworkService.update_reputation(db, worker.id)
        elif status_value == "failed":
            requester_wallet = WalletService.get_wallet(db, WalletOwnerType.agent, str(requester.id))
            if requester_wallet:
                WalletService.unlock_tokens(db, requester_wallet, float(contract.payment_amount))
            AgentNetworkService.update_reputation(db, worker.id)

        return contract

    @staticmethod
    def create_workflow(db: Session, name: str, description: str | None, steps: list[dict]) -> AgentWorkflow:
        workflow = AgentWorkflow(name=name, description=description)
        db.add(workflow)
        db.flush()
        for step in steps:
            db.add(
                WorkflowStep(
                    workflow_id=workflow.id,
                    step_order=step["step_order"],
                    agent_id=step["agent_id"],
                    task_prompt=step["task_prompt"],
                )
            )
        return workflow

    @staticmethod
    def list_workflows(db: Session) -> list[AgentWorkflow]:
        return db.query(AgentWorkflow).order_by(AgentWorkflow.created_at.desc()).all()

    @staticmethod
    def list_workflow_steps(db: Session, workflow_id: int) -> list[WorkflowStep]:
        return db.query(WorkflowStep).filter(WorkflowStep.workflow_id == workflow_id).order_by(WorkflowStep.step_order.asc()).all()

    @staticmethod
    def create_schedule(db: Session, agent_id: UUID, cron_expression: str, task_prompt: str, enabled: bool) -> AgentSchedule:
        schedule = AgentSchedule(agent_id=agent_id, cron_expression=cron_expression, task_prompt=task_prompt, enabled=enabled)
        db.add(schedule)
        return schedule

    @staticmethod
    def list_schedules(db: Session) -> list[AgentSchedule]:
        return db.query(AgentSchedule).order_by(AgentSchedule.created_at.desc()).all()

    @staticmethod
    def update_reputation(db: Session, agent_id: UUID) -> AgentReputation:
        contracts = (
            db.query(AgentTask)
            .filter(AgentTask.worker_agent_id == agent_id, AgentTask.requester_agent_id.is_not(None))
            .all()
        )
        total = len(contracts)
        completed = sum(1 for task in contracts if task.status == "completed")
        success_rate = (completed / total) if total else 0

        completion_durations = []
        for task in contracts:
            if task.completed_at and task.created_at:
                completion_durations.append((task.completed_at - task.created_at).total_seconds())
        avg_duration_seconds = (sum(completion_durations) / len(completion_durations)) if completion_durations else 0

        agent = db.query(ManagedAgent).filter(ManagedAgent.id == agent_id).first()
        market_rating = float(agent.average_rating or 0) / 5 if agent else 0
        time_score = max(0, 1 - (avg_duration_seconds / 86400)) if avg_duration_seconds else 1
        score = round(((success_rate * 0.5) + (market_rating * 0.3) + (time_score * 0.2)) * 100, 2)

        reputation = db.query(AgentReputation).filter(AgentReputation.agent_id == agent_id).first()
        if not reputation:
            reputation = AgentReputation(agent_id=agent_id)
            db.add(reputation)

        reputation.score = score
        reputation.tasks_completed = completed
        reputation.success_rate = round(success_rate * 100, 2)
        reputation.updated_at = datetime.utcnow()
        return reputation

    @staticmethod
    def get_reputation(db: Session, agent_id: UUID) -> AgentReputation:
        reputation = db.query(AgentReputation).filter(AgentReputation.agent_id == agent_id).first()
        if reputation:
            return reputation
        return AgentNetworkService.update_reputation(db, agent_id)
