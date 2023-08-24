from celery import Celery
from utils.redis import get_redis_conn


celery = Celery(
    __name__,
    broker=get_redis_conn(),
    backend=get_redis_conn(),
)
