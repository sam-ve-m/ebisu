from typing import List

from src.domain.enums.region import Region
from src.repositories.user_positions.repository import UserPositionsRepository
from src.transport.drive_wealth.position.transport import DwPositionTransport


class UserPositionsService:
    positions_repository = UserPositionsRepository
    dw_transport = DwPositionTransport

    @classmethod
    async def count_positions_by_region(cls, region: str, accounts: List[str]):
        get_positions_per_region = {
            Region.BR.value: cls.count_positions_br,
            Region.US.value: cls.count_positions_us,
        }
        get_position = get_positions_per_region.get(region)
        positions = await get_position(accounts)
        return positions

    @classmethod
    async def count_positions_br(cls, accounts: List[str]) -> int:
        positions = await cls.positions_repository.get_positions(accounts)
        number_of_positions = len(positions)
        return number_of_positions

    @classmethod
    async def count_positions_us(cls, accounts: List[str]):
        positions = await cls.dw_transport.get_positions(accounts)
        number_of_positions = len(positions)
        return number_of_positions
