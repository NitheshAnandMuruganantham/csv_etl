import redis
from bootstrap_config import app_config, bootstrap_config


def get_redis_conn():
    bootstrap_config()
    return f"redis://default:{app_config['REDIS_PASSWORD']}@{app_config['REDIS_URL']}:{app_config['REDIS_PORT']}"


def get_redis():
    return redis.Redis(
        host=app_config['REDIS_URL'],
        port=app_config['REDIS_PORT'],
        password=app_config['REDIS_PASSWORD'],
        charset="utf-8",
        decode_responses=True
    )
