from src.domain.validators.exchange_info.get_balance_validator import GetBalanceModel
from src.repositories.statements.repository import StatementsRepository
from src.domain.enums.region import Region
from src.services.get_balance.strategies import balance_region


class GetBalance:

    oracle_singleton_instance = StatementsRepository

    @staticmethod
    def get_accounts_by_region(portfolios: dict, region: str) -> str:
        accounts_by_region = {
            Region.BR.value: "bmf_account",
            Region.US.value: "dw_account",
        }
        field = accounts_by_region[region]
        return portfolios.get(field)


    @classmethod
    async def get_service_response(cls, balance: GetBalanceModel, jwt_data: dict) -> dict:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})

        region = balance.region.value
        region_portfolios = portfolios.get(region.lower(), {})

        accounts = cls.get_accounts_by_region(region_portfolios, region)
        balance_resolver = balance_region[region]

        balance = await balance_resolver.get_balance(accounts)

        return balance
