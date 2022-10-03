from src.infrastructures.env_config import config
from src.infrastructures.redis.infraestructure import RedisInfrastructure
from src.domain.models.forex.balance.model import AllowedWithdraw, WithdrawValues


class ForexBalanceRepository(RedisInfrastructure):

    host = config("REDIS_HOST_URL")
    db = config("REDIS_BALANCE_DB")

    @classmethod
    async def get_allowed_to_withdraw(
        cls, redis_hash: str
    ) -> AllowedWithdraw:
        redis = await cls.get_redis()
        keys = await redis.keys(redis_hash)
        values = await redis.mget(keys)
        values_decoded = [eval(value.decode()) for value in values]
        withdraw_values = WithdrawValues(values_decoded)
        allowed_withdraw = AllowedWithdraw(withdraw_values=withdraw_values)
        return allowed_withdraw
