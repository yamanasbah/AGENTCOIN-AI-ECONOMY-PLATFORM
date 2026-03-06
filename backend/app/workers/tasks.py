from datetime import datetime

from app.db.session import SessionLocal
from app.modules.agent_network.models import AgentSchedule
from app.modules.agents.models import AgentTask, ManagedAgent
from app.modules.notifications.service import NotificationService
from app.workers.celery_app import celery_app


def _cron_matches_now(cron_expression: str, now: datetime) -> bool:
    parts = cron_expression.strip().split()
    if len(parts) != 5:
        return False

    def match(token: str, value: int) -> bool:
        if token == "*":
            return True
        if token.startswith("*/"):
            step = int(token.split("/", 1)[1])
            return value % step == 0
        if "," in token:
            return any(match(chunk.strip(), value) for chunk in token.split(","))
        return token.isdigit() and int(token) == value

    minute, hour, day, month, weekday = parts
    weekday_value = (now.weekday() + 1) % 7
    return all(
        [
            match(minute, now.minute),
            match(hour, now.hour),
            match(day, now.day),
            match(month, now.month),
            match(weekday, weekday_value),
        ]
    )


@celery_app.task(name="app.workers.tasks.execute_agent_task")
def execute_agent_task(task_id: int) -> dict:
    from app.tasks.run_agent_task import run_agent

    db = SessionLocal()
    try:
        task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
        if not task:
            return {"status": "task_not_found"}

        task.status = "running"
        db.commit()

        result = run_agent(str(task.agent_id), task.payload.get("input", ""))
        task.status = "completed" if result.get("status") == "completed" else "failed"
        task.finished_at = datetime.utcnow()
        task.completed_at = task.finished_at

        agent = db.query(ManagedAgent).filter(ManagedAgent.id == task.agent_id).first()
        if agent:
            NotificationService.create_notification(
                db,
                agent.owner_user_id,
                "Agent task finished",
                f"Task #{task.id} for agent '{agent.name}' ended with status: {task.status}.",
            )
        db.commit()
        return {"task_id": task.id, **result}
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        return {"status": "failed", "error": str(exc)}
    finally:
        db.close()


@celery_app.task(name="app.workers.tasks.schedule_autonomous_agents")
def schedule_autonomous_agents() -> dict:
    db = SessionLocal()
    scheduled = 0
    try:
        now = datetime.utcnow()
        agents = db.query(ManagedAgent).filter(ManagedAgent.is_autonomous.is_(True)).all()
        for agent in agents:
            if agent.last_run_at is None or (now - agent.last_run_at).total_seconds() >= agent.run_interval_seconds:
                task = AgentTask(
                    agent_id=agent.id,
                    task_type="autonomous_run",
                    payload={"input": ""},
                    status="pending",
                )
                db.add(task)
                db.flush()
                execute_agent_task.delay(task.id)
                scheduled += 1
        db.commit()
        return {"status": "scheduled", "count": scheduled}
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        return {"status": "failed", "error": str(exc)}
    finally:
        db.close()


@celery_app.task(name="app.workers.tasks.schedule_agent_network_tasks")
def schedule_agent_network_tasks() -> dict:
    db = SessionLocal()
    scheduled = 0
    try:
        now = datetime.utcnow().replace(second=0, microsecond=0)
        schedules = db.query(AgentSchedule).filter(AgentSchedule.enabled.is_(True)).all()
        for schedule in schedules:
            if _cron_matches_now(schedule.cron_expression, now):
                task = AgentTask(
                    agent_id=schedule.agent_id,
                    task_type="scheduled_network_run",
                    payload={"input": schedule.task_prompt},
                    status="pending",
                )
                db.add(task)
                db.flush()
                execute_agent_task.delay(task.id)
                scheduled += 1
        db.commit()
        return {"status": "scheduled", "count": scheduled}
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        return {"status": "failed", "error": str(exc)}
    finally:
        db.close()


@celery_app.task(name="app.workers.tasks.run_agent_task")
def run_agent_task(agent_id: str, user_input: str = "") -> dict:
    from app.tasks.run_agent_task import run_agent

    return run_agent(agent_id, user_input)


@celery_app.task(name="app.workers.tasks.run_agent")
def run_agent_alias(agent_id: str, user_input: str = "") -> dict:
    return run_agent_task(agent_id, user_input)


@celery_app.task(name="app.workers.tasks.run_agent_strategy")
def run_agent_strategy(agent_id: str) -> dict:
    return run_agent_task(agent_id, "")
