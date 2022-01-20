import json

from aioredis.client import Redis


class RedisRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def add(self, queue_key: str, data: str):
        await self.redis.lpush(queue_key, data)

    async def get_data(self, queue_key: str):
        data = await self.redis.rpop(queue_key)
        if not data:
            return
        return json.loads(data)

    async def has_data(self, queue_key: str):
        size = await self.redis.llen(queue_key)
        if size > 0:
            return True
        return False
