from src.domain.enums.currency import Currency
from typing import Tuple
from src.infrastructures.redis.infraestructure import RedisInfrastructure
from src.infrastructures.env_config import config
from src.domain.exceptions.model import NotMappedCurrency


class RealtimeFundingAndWithdrawalRepository(RedisInfrastructure):

    host = config("FUNDING_AND_WITHDRAWAL_REDIS_HOST_URL")
    db = config("FUNDING_AND_WITHDRAWAL_REDIS_CACHE_DB")

    @classmethod
    async def get_tax(cls, cash_conversion: Tuple[Currency, Currency]) -> float:
        key = cls.generate_key(cash_conversion=cash_conversion, data_type="tax")
        redis = cls.get_redis()
        binary_value = await redis.get(name=key)
        if not isinstance(binary_value, bytes):
            raise NotMappedCurrency()
        value = float(binary_value.decode())
        return value

    @classmethod
    async def get_spread(cls, cash_conversion: Tuple[Currency, Currency]) -> float:
        key = cls.generate_key(cash_conversion=cash_conversion, data_type="spread")
        redis = cls.get_redis()
        binary_value = await redis.get(name=key)
        if not isinstance(binary_value, bytes):
            raise NotMappedCurrency()
        value = float(binary_value.decode())
        return value

    @classmethod
    async def get_currency_quote(
        cls, cash_conversion: Tuple[Currency, Currency]
    ) -> float:
        key = cls.generate_key(
            cash_conversion=cash_conversion, data_type="currency_quote"
        )
        redis = cls.get_redis()
        binary_value = await redis.get(name=key)
        if not isinstance(binary_value, bytes):
            raise NotMappedCurrency()
        value = float(binary_value.decode())
        return value

    @classmethod
    def generate_key(
        cls, cash_conversion: Tuple[Currency, Currency], data_type: str
    ) -> str:
        cash_conversion_str = ">".join([currency.value for currency in cash_conversion])
        return f"{cash_conversion_str}:{data_type}"
