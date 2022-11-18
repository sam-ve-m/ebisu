from typing import Union

from persephone_client import Persephone

from src.domain.enums.persephone import PersephoneQueue, PersephoneSchema
from src.domain.enums.region import Region
from src.domain.exceptions.service.auditing_trail.model import FailToSaveAuditingTrail
from src.domain.models.account.bank.model import BankAccount
from src.domain.models.account.broker.model import BrokerAccount
from src.domain.models.device_info.dto import DeviceInfo
from src.domain.models.thebes_answer.model import ThebesAnswer
from src.domain.request.funding_and_withdrawal.validators import (
    UserMoneyFlowSameExchange,
    UserMoneyFlowDifferentExchange,
    UserMoneyFlowToExternalBank,
)
from nidavellir import Sindri

from src.infrastructures.env_config import config
from src.services.funding_and_withdraw.money_flow_resolvers import (
    TransferToExternalBank,
)
from src.transport.device_info.transport import DeviceSecurity


class FundingAndWithdrawalService:
    @classmethod
    async def withdrawal_to_external_bank(
        cls,
        money_flow: UserMoneyFlowToExternalBank,
        jwt: ThebesAnswer,
        origin_account: BrokerAccount,
        account_destination: BankAccount,
        device_info: DeviceInfo,
    ):

        await cls._log_in_persephone_to_audit(
            money_flow=money_flow,
            jwt=jwt,
            origin_account=origin_account,
            account_destination=account_destination,
            device_info=device_info,
        )

        transfer_to_external_bank = TransferToExternalBank(
            origin_account=origin_account,
            account_destination=account_destination,
            value=money_flow.value,
        )

        resume = await transfer_to_external_bank()

        return resume

    @staticmethod
    async def _log_in_persephone_to_audit(
            money_flow: UserMoneyFlowToExternalBank,
            jwt: ThebesAnswer,
            origin_account: BrokerAccount,
            account_destination: BankAccount,
            device_info: DeviceInfo,
    ):
        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_MONEY_MOVEMENT_TRANSFERENCE"),
            partition=PersephoneQueue.CASH_FLOW_WITHDRAWAL_TO_EXTERNAL_BANK.value,
            message={
                "unique_id": jwt.unique_id,
                "origin_account": origin_account.resume(),
                "account_destination": account_destination.resume(),
                "value": money_flow.value,
                "device_id": device_info.device_id,
                "device_info": device_info.decrypted_device_info,
            },
            schema_name=PersephoneSchema.CASH_FLOW_WITHDRAWAL_TO_EXTERNAL_BANK.value,
        )
        if sent_to_persephone is False:
            raise FailToSaveAuditingTrail("common.process_issue")

    @classmethod
    async def money_flow_between_user_dtvm_accounts(
        cls,
        money_flow: Union[UserMoneyFlowSameExchange, UserMoneyFlowDifferentExchange],
        jwt_data: dict,
    ):
        jwt = ThebesAnswer(jwt_data=jwt_data)
        jwt.account_br_is_blocked()
        unique_id = jwt.unique_id

        origin_account = BrokerAccount(
            **money_flow.origin_account.dict(),
            user_unique_id=unique_id,
        )
        account_destination = BrokerAccount(
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
