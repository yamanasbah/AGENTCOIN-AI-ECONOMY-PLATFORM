from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "agentcoin",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.run_agent_task", "app.workers.tasks"],
)
celery_app.conf.task_routes = {
    "app.tasks.run_agent_task.*": {"queue": "runtime"},
    "app.workers.tasks.*": {"queue": "agentcoin"},
}

celery_app.conf.beat_schedule = {
    "schedule-autonomous-agents": {
        "task": "app.workers.tasks.schedule_autonomous_agents",
        "schedule": 60.0,
    },
    "schedule-agent-network-tasks": {
        "task": "app.workers.tasks.schedule_agent_network_tasks",
        "schedule": 60.0,
    },
}
