import redis
from tqdm import tqdm
from settings import settings


class RedisService:
    def __init__(self, db):
        self.client = redis.Redis(
            host=settings.REDIS_URL, password=settings.REDIS_PASSWORD, port=settings.REDIS_PORT, db=0)
        self.db = db

    def search(self, search_type, search):
        print(f"Searching {search_type}")
        results = []
        keys = self.client.keys(search_type + search + "*")
        for key in keys:
            results.append(dict(self.client.hgetall(key)))
        return results
