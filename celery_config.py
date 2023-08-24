from loguru import logger
from utils.redis import get_redis_conn
from bootstrap_config import bootstrap_config
from utils.celery import celery
import tasks.validation as validation_workers

bootstrap_config()

celery.autodiscover_tasks(['tasks'])


def reschedule_task(params, function):
    logger.info(
        f"Rescheduling task {function} for req id {params.get('req_id')} and block id {params.get('block_id')}")
    function.delay(params)
