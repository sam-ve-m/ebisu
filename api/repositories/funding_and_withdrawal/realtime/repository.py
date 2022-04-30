from api.domain.enums.currency import Currency
from typing import Tuple
from api.infrastructures.redis.infraestructure import RedisInfrastructure
from api.infrastructures.env_config import config

class RealtimeFundingAndWithdrawalRepository(RedisInfrastructure):

    host = config("FUNDING_AND_WITHDRAWAL_REDIS_HOST_URL")
    db = config("FUNDING_AND_WITHDRAWAL_REDIS_CACHE_DB")

    @classmethod
    async def get_tax(cls, cash_conversion: Tuple[Currency, Currency]) -> float:
        key = cls.generate_key(cash_conversion=cash_conversion, data_type="tax")
        redis = cls.get_redis()
        binary_value = await redis.get(name=key)
        value = float(binary_value.decode())
        return value

    @classmethod
    async def get_spread(cls, cash_conversion: Tuple[Currency, Currency]) -> float:
        key = cls.generate_key(cash_conversion=cash_conversion, data_type="spread")
        redis = cls.get_redis()
        binary_value = await redis.get(name=key)
        value = float(binary_value.decode())
        return value

    @classmethod
    async def get_currency_quote(cls, cash_conversion: Tuple[Currency, Currency]) -> float:
        key = cls.generate_key(cash_conversion=cash_conversion, data_type="currency_quote")
        redis = cls.get_redis()
        binary_value = await redis.get(name=key)
        value = float(binary_value.decode())
        return value

    @classmethod
    def generate_key(cls, cash_conversion: Tuple[Currency, Currency], data_type: str) -> str:
        from_currency = cash_conversion[0].value
        to_currency = cash_conversion[1].value
        return f"{from_currency}>{to_currency}:{data_type}"
