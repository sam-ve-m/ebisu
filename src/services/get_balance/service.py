from src.domain.balance.base.model import BaseBalance
from src.domain.enums.region import Region
from src.repositories.balance.repository import BalanceRepository
from src.transport.drive_wealth.balance.transport import DwBalanceTransport
from src.domain.validators.exchange_info.get_balance_validator import GetBalanceModel


class BalanceService:

    balance_region = {
        "BR": BalanceRepository.get_balance,
        "US": DwBalanceTransport.get_balance,
    }

    @staticmethod
    def get_accounts_by_region(portfolios: dict, region: str) -> str:
        accounts_by_region = {
            Region.BR.value: "bmf_account",
            Region.US.value: "dw_account",
        }
        field = accounts_by_region[region]
        return portfolios.get(field)

    @classmethod
    async def get_service_response(
        cls, balance: GetBalanceModel, jwt_data: dict
    ) -> BaseBalance:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        region = balance.region.value
        region_portfolios = portfolios.get(region.lower(), {})
        account = cls.get_accounts_by_region(region_portfolios, region)

        balance_resolver = cls.balance_region[region]
        balance = await balance_resolver(account)

        return balance
