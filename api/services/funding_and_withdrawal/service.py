import asyncio
from typing import Callable, List
from api.domain.enums.region import Region
from api.domain.exception.model import MoneyFlowResolverNoFoundError, InvalidAccountsOwnership
from api.repositories.user.repository import UserRepository


class FundingAndWithdrawalService:

    @classmethod
    async def money_flow_between_user_dtvm_accounts(cls, money_flow_between_user_accounts_request_data: dict):
        origin_account_number = money_flow_between_user_accounts_request_data["origin_account"]["account_number"]
        account_destination_number = money_flow_between_user_accounts_request_data["account_destination"]["account_number"]
        unique_id = money_flow_between_user_accounts_request_data["x-thebes-answer"]["user"]["unique_id"]

        await cls._validate_accounts_ownership(
            user_unique_id=unique_id,
            accounts=[origin_account_number, account_destination_number]
        )

        validate_primary_account = [
            cls._is_primary_account(user_unique_id=unique_id, account_number=origin_account_number),
            cls._is_primary_account(user_unique_id=unique_id, account_number=account_destination_number),
        ]
        (
            is_origin_account_primary_account,
            is_account_destination_primary_account
        ) = await asyncio.gather(*validate_primary_account)

        origin_account_region = money_flow_between_user_accounts_request_data["origin_account"]["country"]
        account_destination_region = money_flow_between_user_accounts_request_data["account_destination"]["country"]

        money_flow_callable = await cls._get_money_flow_resolver(
            origin_account_region=origin_account_region,
            is_origin_account_primary_account=is_origin_account_primary_account,
            account_destination_region=account_destination_region,
            is_account_destination_primary_account=is_account_destination_primary_account,
        )

        resume = await money_flow_callable()

    @classmethod
    async def _get_money_flow_resolver(
            cls,
            origin_account_region: Region,
            is_origin_account_primary_account: bool,
            account_destination_region: Region,
            is_account_destination_primary_account: bool
    ) -> Callable:
        origin_account_fingerprint = (origin_account_region, is_origin_account_primary_account)
        account_destination_fingerprint = (account_destination_region, is_account_destination_primary_account)
        money_flow_fingerprint = (origin_account_fingerprint, account_destination_fingerprint)
        money_flow_resolver_map = {
            # ((Region.BR, True), (Region.BR, False)): cls.transfers_between_sinacor_accounts,
            ((Region.BR, True), (Region.US, True)): cls.transfers_between_sinacor_and_drive_wealth,
            # ((Region.BR, True), (Region.US, False)): cls.transfers_between_sinacor_and_drive_wealth,
            # ((Region.BR, False), (Region.BR, True)): cls.transfers_between_sinacor_accounts,
            # ((Region.US, False), (Region.BR, True)): cls.transfers_between_drive_wealth_and_sinacor,
            ((Region.US, True), (Region.BR, True)): cls.transfers_between_drive_wealth_and_sinacor,
        }
        if money_flow_resolver := money_flow_resolver_map.get(money_flow_fingerprint):
            return money_flow_resolver
        raise MoneyFlowResolverNoFoundError()


    @classmethod
    async def transfers_between_sinacor_accounts(cls):
        pass

    @classmethod
    async def transfers_between_sinacor_and_drive_wealth(cls):
        pass

    @classmethod
    async def transfers_between_drive_wealth_and_sinacor(cls):
        pass
