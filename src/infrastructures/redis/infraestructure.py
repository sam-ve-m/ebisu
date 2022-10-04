# OUTSIDE LIBRARIES
import redis.asyncio as aioredis


class RedisInfrastructure:
    redis = None
    host = None
    db = None

    @classmethod
    def get_redis(cls):
        if cls.redis is None:
            url = f"{cls.host}?db={cls.db}"

            cls.redis = aioredis.from_url(url)
        return cls.redis
