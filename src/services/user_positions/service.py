from typing import List

from src.domain.enums.region import Region
from src.domain.positions.model import Position
from src.repositories.user_positions.repository import UserPositionsRepository
from src.transport.drive_wealth.position.transport import DwPositionTransport


class UserPositionsService:

    positions_per_region = {
        Region.BR.value: UserPositionsRepository,
        Region.US.value: DwPositionTransport,
    }

    @staticmethod
    def get_account_by_region(portfolios: dict, region: str) -> str:
        accounts_by_region = {
            Region.BR.value: "bmf_account",
            Region.US.value: "dw_account",
        }
        field = accounts_by_region[region]
        return portfolios.get(field)

    @classmethod
    async def get_positions_by_region(
        cls, region: str, jwt_data: dict
    ) -> List[Position]:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        region_portfolios = portfolios.get(region.lower(), {})
        account = cls.get_account_by_region(portfolios=region_portfolios, region=region)

        position_resolver = cls.positions_per_region.get(region)
        positions = await position_resolver.get_positions(account)
        return positions
