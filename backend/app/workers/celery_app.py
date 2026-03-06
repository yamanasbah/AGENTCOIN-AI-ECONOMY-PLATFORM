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
