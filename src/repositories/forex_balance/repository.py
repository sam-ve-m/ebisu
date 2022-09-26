from src.infrastructures.env_config import config
from src.infrastructures.redis.infraestructure import RedisInfrastructure
from src.domain.models.forex.balance.model import AllowedWithdraw


class ForexBalanceRepository(RedisInfrastructure):

    host = config("REDIS_HOST_URL")
    db = config("REDIS_BALANCE_DB")

    @classmethod
    async def get_allowed_to_withdraw(
        cls, balance_hash: str
    ) -> AllowedWithdraw:
        redis = await cls.get_redis()
        keys = await redis.keys(balance_hash)
        values = await redis.mget(keys)
        allowed_withdraw = AllowedWithdraw(values=values)
        return allowed_withdraw


# from src.domain.enums.forex.countrys import Country
# from src.domain.enums.forex.composition_hash_options import Wallet, Balance
# import asyncio
#
#
# allowed_to_withdraw = asyncio.run(ForexBalanceRepository.get_allowed_to_withdraw(balance_hash=f"4e2617aa-2700-4fd4-acb6-47bc64362aa4:{Country.BR.lower()}:932:{Wallet.BALANCE}:"
#                                f"{Balance.ALLOWED_TO_WITHDRAW}:*"))
# print(allowed_to_withdraw.total_available)