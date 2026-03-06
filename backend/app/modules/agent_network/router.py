from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.agent_network.schemas import (
    AgentCapabilityCreate,
    AgentCapabilityRead,
    AgentDiscoveryResult,
    AgentReputationRead,
    AgentScheduleCreate,
    AgentScheduleRead,
    AgentTaskContractCreate,
    AgentTaskContractRead,
    WorkflowCreate,
    WorkflowRead,
)
from app.modules.agent_network.service import AgentNetworkService

router = APIRouter()


@router.post("/capabilities", response_model=AgentCapabilityRead)
def create_capability(payload: AgentCapabilityCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    capability = AgentNetworkService.create_capability(db, payload.agent_id, payload.capability_name, payload.description)
    db.commit()
    db.refresh(capability)
    return capability


@router.get("/capabilities", response_model=list[AgentCapabilityRead])
def list_capabilities(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return AgentNetworkService.list_capabilities(db)


@router.get("/agents/by-capability/{capability}", response_model=list[AgentDiscoveryResult])
def get_agents_by_capability(
    capability: str,
    rank_by: str = Query(default="rating", pattern="^(rating|cost)$"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return AgentNetworkService.discover_agents(db, capability, rank_by=rank_by)


@router.post("/contracts", response_model=AgentTaskContractRead)
def create_contract(payload: AgentTaskContractCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = AgentNetworkService.create_task_contract(
        db,
        requester_agent_id=payload.requester_agent_id,
        worker_agent_id=payload.worker_agent_id,
        task_description=payload.task_description,
        payment_amount=payload.payment_amount,
        current_user_id=current_user.id,
    )
    db.commit()
    db.refresh(contract)
    return contract


@router.patch("/contracts/{contract_id}", response_model=AgentTaskContractRead)
def update_contract_status(contract_id: int, status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contract = AgentNetworkService.update_contract_status(db, contract_id, status, current_user.id)
    db.commit()
    db.refresh(contract)
    return contract


@router.post("/workflows", response_model=WorkflowRead)
def create_workflow(payload: WorkflowCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    workflow = AgentNetworkService.create_workflow(db, payload.name, payload.description, [step.model_dump() for step in payload.steps])
    db.commit()
    steps = AgentNetworkService.list_workflow_steps(db, workflow.id)
    return WorkflowRead(
        id=workflow.id,
        name=workflow.name,
        description=workflow.description,
        created_at=workflow.created_at,
        steps=steps,
    )


@router.get("/workflows", response_model=list[WorkflowRead])
def list_workflows(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    workflows = AgentNetworkService.list_workflows(db)
    result = []
    for workflow in workflows:
        steps = AgentNetworkService.list_workflow_steps(db, workflow.id)
        result.append(
            WorkflowRead(
                id=workflow.id,
                name=workflow.name,
                description=workflow.description,
                created_at=workflow.created_at,
                steps=steps,
            )
        )
    return result


@router.post("/schedules", response_model=AgentScheduleRead)
def create_schedule(payload: AgentScheduleCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    schedule = AgentNetworkService.create_schedule(db, payload.agent_id, payload.cron_expression, payload.task_prompt, payload.enabled)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.get("/schedules", response_model=list[AgentScheduleRead])
def list_schedules(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return AgentNetworkService.list_schedules(db)


@router.get("/agents/{agent_id}/reputation", response_model=AgentReputationRead)
def get_reputation(agent_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    reputation = AgentNetworkService.get_reputation(db, agent_id)
    db.commit()
    db.refresh(reputation)
    return reputation
