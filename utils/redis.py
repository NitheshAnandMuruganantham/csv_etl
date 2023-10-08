import redis
from settings import settings


def get_redis_conn():
    return f"redis://default:{settings.REDIS_PASSWORD}@{settings.REDIS_URL}:{settings.REDIS_PORT}"


def get_redis():
    return redis.Redis(
        host=settings.REDIS_URL,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        charset="utf-8",
        decode_responses=True
    )
