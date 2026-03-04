from app.services.onchain_sync_service import sync_placeholder
from app.workers.celery_app import celery_app


@celery_app.task
def run_onchain_sync() -> str:
    sync_placeholder()
    return "sync_complete"
