
from loguru import logger
from utils.redis import get_redis


def enqueue(element, queue_key):
    redis_client = get_redis()
    redis_client.rpush(queue_key, element)
    logger.info(f"Enqueued {element} in {queue_key}")
    logger.info(redis_client.lrange(queue_key, 0, -1))


def dequeue(queue_key):
    redis_client = get_redis()
    return redis_client.lpop(queue_key)


def remove_element(element, queue_key):
    redis_client = get_redis()
    redis_client.lrem(queue_key, 0, element)


def get_first_element(queue_key):
    redis_client = get_redis()
    unordered_list = redis_client.lrange(queue_key, 0, -1)
    sorted_list = sorted(unordered_list)
    if len(sorted_list) == 0:
        return None
    result = str(sorted_list[0])
    logger.info(
        f"First element in {queue_key} is {result} of type {type(result)}")
    return result


def update_running_status(key, status):
    redis_client = get_redis()
    redis_client.set(key, status)
