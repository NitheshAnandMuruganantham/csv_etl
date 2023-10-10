from celery import Celery
from utils.redis import get_redis_conn
from settings import settings
celery = Celery(
    __name__,
    broker=settings.RABITMQ_URL,
    backend=get_redis_conn(),
)
