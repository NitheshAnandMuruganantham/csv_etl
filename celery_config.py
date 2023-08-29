from bootstrap_config import bootstrap_config
from utils.celery import celery
import tasks.validation as validation_workers
import tasks.process as process_workers

bootstrap_config()

celery.autodiscover_tasks(['tasks'])
