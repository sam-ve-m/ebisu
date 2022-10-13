from typing import Union

from src.domain.enums.region import Region
from src.domain.models.account.bank import BankAccount
from src.domain.models.account.exchanges import ExchangeAccount
from src.domain.validators.funding_and_withdrawal.validators import (
    UserMoneyFlowSameExchange,
    UserMoneyFlowDifferentExchange,
    UserMoneyFlowToExternalBank,
)
from nidavellir import Sindri

from src.services.funding_and_withdrawal.money_flow_resolvers import (
    TransferToExternalBank,
)


class FundingAndWithdrawalService:
    @classmethod
    async def withdrawal_to_external_bank(
        cls, money_flow: UserMoneyFlowToExternalBank, jwt_data: dict
    ):
        unique_id = jwt_data["user"]["unique_id"]

        origin_account = ExchangeAccount(
            account_number=jwt_data["user"]["portfolios"]["br"]["bmf_account"],
            user_unique_id=unique_id,
            country=Region.BR,
        )

        account_destination = BankAccount(
            bank_account_id=str(money_flow.bank_account_id),
            user_unique_id=unique_id,
            country=Region.BR,
        )

        await origin_account.validate_accounts_ownership()
        await account_destination.validate_accounts_ownership()

        transfer_to_external_bank = TransferToExternalBank(
            origin_account=origin_account,
            account_destination=account_destination,
            value=money_flow.value,
        )

        resume = await transfer_to_external_bank()

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

        await account_destination.validate_accounts_ownership()

        def money_flow_resolver_class(*args, **kwargs):
            raise Exception()
            # aplica logica aki de tranferian entre contas sinacor
            async def loro():
                pass

            return loro

        money_flow_resolver = money_flow_resolver_class(
            origin_account=origin_account,
            account_destination=account_destination,
            value=money_flow.value,
        )
        resume = await money_flow_resolver()
        Sindri.dict_to_primitive_types(resume)
        return resume
