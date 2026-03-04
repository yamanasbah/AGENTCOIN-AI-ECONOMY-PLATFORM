from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def sync_placeholder() -> None:
    logger.info("On-chain sync placeholder executed")
