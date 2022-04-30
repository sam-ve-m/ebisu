import asyncio
from typing import Type

from api.domain.abstract_classes.services.funding_and_withdrawal.money_flow_resolvers.abstract_class import \
    MoneyFlowResolverAbstract
from api.domain.enums.region import Region
from api.domain.exception.model import MoneyFlowResolverNoFoundError
from api.domain.model.internal.account_transfer.model import AccountTransfer
from api.repositories.user.repository import UserRepository
from api.services.funding_and_withdrawal.money_flow_resolvers.transfers_between_drive_wealth_and_sinacor import \
    TransfersBetweenDriveWealthAndSinacor
from api.services.funding_and_withdrawal.money_flow_resolvers.transfers_between_sinacor_and_drive_wealth import \
    TransfersBetweenSinacorAndDriveWealth
from nidavellir import Sindri


class FundingAndWithdrawalService:

    @classmethod
    async def money_flow_between_user_dtvm_accounts(cls, money_flow_between_user_accounts_request_data: dict, user_repository=UserRepository):
        unique_id = money_flow_between_user_accounts_request_data["x-thebes-answer"]["user"]["unique_id"]
        user_portfolios = await user_repository.get_user_portfolios(unique_id=unique_id)

        origin_account = AccountTransfer(**money_flow_between_user_accounts_request_data["origin_account"], user_portfolios=user_portfolios)
        account_destination = AccountTransfer(**money_flow_between_user_accounts_request_data["account_destination"], user_portfolios=user_portfolios)

        origin_account_fingerprint = origin_account.validate_accounts_ownership().validate_that_is_primary_account().get_fingerprint()
        account_destination_fingerprint = account_destination.validate_accounts_ownership().validate_that_is_primary_account().get_fingerprint()

        money_flow_resolver_class = await cls._get_money_flow_resolver(
            origin_account_fingerprint=origin_account_fingerprint,
            account_destination_fingerprint=account_destination_fingerprint
        )

        money_flow_resolver = money_flow_resolver_class(
            origin_account=origin_account,
            account_destination=account_destination,
            value=money_flow_between_user_accounts_request_data["value"]
        )
        resume = await money_flow_resolver()
        Sindri.dict_to_primitive_types(resume)
        return resume

    @classmethod
    async def _get_money_flow_resolver(
            cls,
            origin_account_fingerprint: tuple,

            account_destination_fingerprint: tuple,
    ) -> Type[MoneyFlowResolverAbstract]:
        money_flow_fingerprint = (origin_account_fingerprint, account_destination_fingerprint)
        money_flow_resolver_map = {
            # ((Region.BR, True), (Region.BR, False)): cls.transfers_between_sinacor_accounts,
            ((Region.BR, True), (Region.US, True)): TransfersBetweenSinacorAndDriveWealth,
            # ((Region.BR, True), (Region.US, False)): cls.transfers_between_sinacor_and_drive_wealth,
            # ((Region.BR, False), (Region.BR, True)): cls.transfers_between_sinacor_accounts,
            # ((Region.US, False), (Region.BR, True)): cls.transfers_between_drive_wealth_and_sinacor,
            ((Region.US, True), (Region.BR, True)): TransfersBetweenDriveWealthAndSinacor,
        }
        if money_flow_resolver := money_flow_resolver_map.get(money_flow_fingerprint):
            return money_flow_resolver
        raise MoneyFlowResolverNoFoundError()
