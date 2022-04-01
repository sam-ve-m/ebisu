from api.services.get_balance.get_balance import GetBalance
from api.domain.enums.region import Region


class GetBalanceController:

    @staticmethod
    async def get(payload: dict, region: Region):
        get_balance_response = await GetBalance.get_service_response(payload=payload, region=region)
        return get_balance_response
