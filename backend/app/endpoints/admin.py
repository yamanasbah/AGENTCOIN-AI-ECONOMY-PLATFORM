from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from time import perf_counter
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin_user, get_current_super_admin_user, get_db
from app.models.models import AgentFlag, FeatureFlag, PlatformTreasury, User
from app.modules.agents.models import AgentModerationStatus, AgentReview, ManagedAgent
from app.modules.wallet.models import Stake, Transaction
from app.workers.celery_app import celery_app

router = APIRouter()

SAFE_MODE = {"enabled": False}
RISK_LIMITS = {"max_global_drawdown": 25}

FLAG_FAILURE_THRESHOLD = 5
FLAG_TOKENS_THRESHOLD = 50_000
FLAG_BAD_REVIEW_THRESHOLD = 10


class FeatureToggleRequest(BaseModel):
    enabled: bool


def _to_float(value: Decimal | int | float | None) -> float:
    if value is None:
        return 0.0
    return float(value)


def _upsert_agent_flag(db: Session, agent_id: UUID, reason: str, flag_count: int) -> None:
    existing = db.query(AgentFlag).filter(AgentFlag.agent_id == agent_id, AgentFlag.reason == reason).first()
    if existing:
        existing.flag_count = max(existing.flag_count, flag_count)
    else:
        db.add(AgentFlag(agent_id=agent_id, reason=reason, flag_count=flag_count))


def _run_abuse_detection(db: Session) -> None:
    window_start = datetime.utcnow() - timedelta(days=7)

    # SQLAlchemy self-join is unnecessary here; use direct aggregate on agent logs.
    from app.modules.agents.models import AgentLog

    failures = (
        db.query(AgentLog.agent_id, func.count(AgentLog.id).label("failure_count"))
        .filter(AgentLog.status != "success", AgentLog.created_at >= window_start)
        .group_by(AgentLog.agent_id)
        .all()
    )
    for row in failures:
        if int(row.failure_count) >= FLAG_FAILURE_THRESHOLD:
            _upsert_agent_flag(db, row.agent_id, "repeated_execution_failures", int(row.failure_count))

    token_usage = (
        db.query(AgentLog.agent_id, func.coalesce(func.sum(AgentLog.tokens_used), 0).label("tokens_used"))
        .filter(AgentLog.created_at >= window_start)
        .group_by(AgentLog.agent_id)
        .all()
    )
    for row in token_usage:
        if _to_float(row.tokens_used) >= FLAG_TOKENS_THRESHOLD:
            _upsert_agent_flag(db, row.agent_id, "excessive_token_consumption", int(_to_float(row.tokens_used)))

    bad_reviews = (
        db.query(AgentReview.agent_id, func.count(AgentReview.id).label("bad_reviews"))
        .filter(AgentReview.rating <= 2)
        .group_by(AgentReview.agent_id)
        .all()
    )
    for row in bad_reviews:
        if int(row.bad_reviews) >= FLAG_BAD_REVIEW_THRESHOLD:
            _upsert_agent_flag(db, row.agent_id, "too_many_bad_reviews", int(row.bad_reviews))

    db.commit()


@router.get("/treasury")
def get_treasury(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    treasury = db.query(PlatformTreasury).first()
    if not treasury:
        raise HTTPException(status_code=404, detail="Treasury not configured")
    return {
        "id": treasury.id,
        "wallet_id": str(treasury.wallet_id),
        "total_revenue": _to_float(treasury.total_revenue),
        "total_distributed": _to_float(treasury.total_distributed),
        "created_at": treasury.created_at,
    }


@router.get("/revenue")
def get_revenue(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    treasury = db.query(PlatformTreasury).first()
    platform_revenue = _to_float(treasury.total_revenue) if treasury else 0.0
    distributed = _to_float(treasury.total_distributed) if treasury else 0.0
    net_revenue = platform_revenue - distributed

    return {
        "platform_revenue": platform_revenue,
        "total_distributed": distributed,
        "net_revenue": net_revenue,
    }


@router.get("/agents/pending")
def list_pending_agents(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    _run_abuse_detection(db)
    agents = db.query(ManagedAgent).filter(ManagedAgent.agent_status == AgentModerationStatus.pending).order_by(ManagedAgent.created_at.asc()).all()
    return [
        {
            "id": str(agent.id),
            "name": agent.name,
            "owner_user_id": agent.owner_user_id,
            "agent_type": agent.agent_type,
            "agent_status": agent.agent_status,
            "created_at": agent.created_at,
        }
        for agent in agents
    ]


@router.get("/agents/flags")
def list_flagged_agents(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    _run_abuse_detection(db)
    flags = db.query(AgentFlag).order_by(AgentFlag.created_at.desc()).all()
    return [
        {
            "id": flag.id,
            "agent_id": str(flag.agent_id),
            "reason": flag.reason,
            "flag_count": flag.flag_count,
            "created_at": flag.created_at,
        }
        for flag in flags
    ]


def _set_agent_status(db: Session, agent_id: UUID, status_value: AgentModerationStatus):
    agent = db.query(ManagedAgent).filter(ManagedAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent.agent_status = status_value
    if status_value in {AgentModerationStatus.rejected, AgentModerationStatus.banned}:
        agent.is_published = False
    db.commit()
    db.refresh(agent)
    return {"id": str(agent.id), "agent_status": agent.agent_status}


@router.post("/agents/{agent_id}/approve")
def approve_agent(
    agent_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return _set_agent_status(db, agent_id, AgentModerationStatus.approved)


@router.post("/agents/{agent_id}/reject")
def reject_agent(
    agent_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    return _set_agent_status(db, agent_id, AgentModerationStatus.rejected)


@router.post("/agents/{agent_id}/ban")
def ban_agent(
    agent_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_super_admin_user),
):
    return _set_agent_status(db, agent_id, AgentModerationStatus.banned)


@router.get("/analytics")
def admin_analytics(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    treasury = db.query(PlatformTreasury).first()
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_agents = db.query(func.count(ManagedAgent.id)).scalar() or 0
    total_runs = db.query(func.coalesce(func.sum(ManagedAgent.total_runs), 0)).scalar() or 0
    total_transactions = db.query(func.count(Transaction.id)).scalar() or 0
    total_tokens_staked = db.query(func.coalesce(func.sum(Stake.amount), 0)).scalar() or 0
    total_marketplace_volume = db.query(func.coalesce(func.sum(ManagedAgent.total_revenue), 0)).scalar() or 0
    platform_revenue = _to_float(treasury.total_revenue) if treasury else 0.0

    return {
        "total_users": int(total_users),
        "total_agents": int(total_agents),
        "total_runs": int(total_runs),
        "total_transactions": int(total_transactions),
        "total_tokens_staked": _to_float(total_tokens_staked),
        "total_marketplace_volume": _to_float(total_marketplace_volume),
        "platform_revenue": platform_revenue,
    }


@router.get("/system-health")
def system_health(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    from app.modules.agents.models import AgentLog

    start = perf_counter()
    db.execute(select(func.now()))
    api_latency_ms = (perf_counter() - start) * 1000

    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)

    successful_runs = (
        db.query(func.count(AgentLog.id))
        .filter(AgentLog.status == "success", AgentLog.created_at >= one_hour_ago)
        .scalar()
        or 0
    )
    execution_rate_per_min = float(successful_runs) / 60.0

    tx_per_min = (
        db.query(func.count(Transaction.id))
        .filter(Transaction.created_at >= one_minute_ago)
        .scalar()
        or 0
    )

    inspect = celery_app.control.inspect(timeout=0.5)
    active = inspect.active() or {}
    reserved = inspect.reserved() or {}
    queue_size = sum(len(tasks) for tasks in active.values()) + sum(len(tasks) for tasks in reserved.values())

    return {
        "api_latency_ms": round(api_latency_ms, 2),
        "queue_size": int(queue_size),
        "agent_execution_rate": round(execution_rate_per_min, 4),
        "wallet_transactions_per_minute": int(tx_per_min),
    }


@router.get("/features")
def get_features(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user),
):
    flags = db.query(FeatureFlag).order_by(FeatureFlag.name.asc()).all()
    return [{"name": f.name, "enabled": f.enabled, "created_at": f.created_at} for f in flags]


@router.patch("/features/{name}")
def patch_feature_flag(
    name: str,
    payload: FeatureToggleRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_super_admin_user),
):
    feature = db.query(FeatureFlag).filter(FeatureFlag.name == name).first()
    if not feature:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    feature.enabled = payload.enabled
    db.commit()
    db.refresh(feature)
    return {"name": feature.name, "enabled": feature.enabled, "created_at": feature.created_at}


@router.post("/safe-mode")
def set_safe_mode(enabled: bool, _: User = Depends(get_current_super_admin_user)):
    SAFE_MODE["enabled"] = enabled
    return SAFE_MODE


@router.post("/risk-limits")
def update_global_risk_limits(max_global_drawdown: int, _: User = Depends(get_current_super_admin_user)):
    RISK_LIMITS["max_global_drawdown"] = max_global_drawdown
    return RISK_LIMITS
