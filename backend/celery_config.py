from utils.celery import celery
import tasks.validation as validation_workers
import tasks.process as process_workers


celery.autodiscover_tasks(['tasks'])
