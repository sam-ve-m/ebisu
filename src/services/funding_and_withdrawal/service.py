from typing import Type, Union

from src.domain.models.account import Fingerprint, IsPrimaryAccount
from src.domain.abstract_classes.services.funding_and_withdrawal.money_flow_resolvers.abstract_class import (
    MoneyFlowResolverAbstract,
)
from src.domain.enums.region import Region
from src.domain.exception.model import MoneyFlowResolverNoFoundError
from src.domain.models.account import ExchangeAccount, BankAccount
from src.domain.validators.funding_and_withdrawal.validators import UserMoneyFlowSameExchange, \
    UserMoneyFlowDifferentExchange, UserMoneyFlowToExternalBank
from nidavellir import Sindri

from src.services.funding_and_withdrawal.money_flow_resolvers import (
    TransferToExternalBank,
    TransfersBetweenDriveWealthAndSinacor,
    TransfersBetweenSinacorAndDriveWealth
)


class FundingAndWithdrawalService:

    @classmethod
    async def withdrawal_to_external_bank(
            cls,
            money_flow: UserMoneyFlowToExternalBank,
            jwt_data: dict
    ):
        unique_id = jwt_data["user"]["unique_id"]

        origin_account = ExchangeAccount(
            account_number=jwt_data["user"]["portfolios"]["br"]["bovespa_account"],
            user_unique_id=unique_id,
            country=Region.BR
        )

        account_destination = BankAccount(
            bank_account_id=str(money_flow.bank_account_id),
            user_unique_id=unique_id,
            country=Region.BR
        )

        await origin_account.validate_accounts_ownership()
        await account_destination.validate_accounts_ownership()

        transfer_to_external_bank = TransferToExternalBank(
            origin_account=origin_account,
            account_destination=account_destination,
            value=money_flow.value
        )

        resume = await transfer_to_external_bank()
        Sindri.dict_to_primitive_types(resume)
        return resume

    @classmethod
    async def money_flow_between_user_dtvm_accounts(
            cls,
            money_flow: Union[UserMoneyFlowSameExchange, UserMoneyFlowDifferentExchange],
            jwt_data: dict,
    ):
        unique_id = jwt_data["user"]["unique_id"]

        origin_account = ExchangeAccount(
            **money_flow.origin_account.dict(),
            user_unique_id=unique_id,
        )
        account_destination = ExchangeAccount(
            **money_flow.account_destination.dict(),
            user_unique_id=unique_id,
        )
        await origin_account.validate_accounts_ownership()
        origin_account_fingerprint = origin_account.get_fingerprint()

        await account_destination.validate_accounts_ownership()
        account_destination_fingerprint = account_destination.get_fingerprint()

        money_flow_resolver_class = await cls._get_money_flow_resolver_between_exchanges(
            origin_account_fingerprint=origin_account_fingerprint,
            account_destination_fingerprint=account_destination_fingerprint,
        )

        money_flow_resolver = money_flow_resolver_class(
            origin_account=origin_account,
            account_destination=account_destination,
            value=money_flow.value,
        )
        resume = await money_flow_resolver()
        Sindri.dict_to_primitive_types(resume)
        return resume

    @classmethod
    async def _get_money_flow_resolver_between_exchanges(
            cls,
            origin_account_fingerprint: Fingerprint,
            account_destination_fingerprint: Fingerprint,
    ) -> Type[MoneyFlowResolverAbstract]:
        money_flow_fingerprint = (
            origin_account_fingerprint,
            account_destination_fingerprint,
        )

        br_primary_account = (Region.BR, IsPrimaryAccount(True))
        br_account = (Region.BR, IsPrimaryAccount(False))
        us_primary_account = (Region.US, IsPrimaryAccount(True))
        us_account = (Region.US, IsPrimaryAccount(False))

        money_flow_resolver_map = {
            # (br_primary_account, br_account): cls.transfers_between_sinacor_accounts,
            (br_primary_account, us_primary_account): TransfersBetweenSinacorAndDriveWealth,
            # (br_primary_account, us_account): cls.transfers_between_sinacor_and_drive_wealth,
            # (br_account, br_primary_account): cls.transfers_between_sinacor_accounts,
            # (us_account, br_primary_account): cls.transfers_between_drive_wealth_and_sinacor,
            (us_primary_account, br_primary_account): TransfersBetweenDriveWealthAndSinacor,
        }
        if money_flow_resolver := money_flow_resolver_map.get(money_flow_fingerprint):
            return money_flow_resolver
        raise MoneyFlowResolverNoFoundError()
