from app.tasks.run_agent_task import run_agent
from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks.run_agent_task")
def run_agent_task(agent_id: str, user_input: str = "") -> dict:
    return run_agent(agent_id, user_input)


@celery_app.task(name="app.workers.tasks.run_agent")
def run_agent_alias(agent_id: str, user_input: str = "") -> dict:
    return run_agent(agent_id, user_input)


@celery_app.task(name="app.workers.tasks.run_agent_strategy")
def run_agent_strategy(agent_id: str) -> dict:
    return run_agent(agent_id, "")
