from http import HTTPStatus

from fastapi import Request, APIRouter
from nidavellir import Sindri

from src.domain.enums.region import Region
from src.domain.enums.response.internal_code import InternalCode
from src.domain.models.account.bank.model import BankAccount
from src.domain.models.account.broker.model import BrokerAccount
from src.domain.models.thebes_answer.model import ThebesAnswer
from src.domain.responses.http_response_model import ResponseModel
from src.domain.request.funding_and_withdrawal.validators import (
    UserMoneyFlowSameExchange,
    UserMoneyFlowToExternalBank,
)
from src.services.device_info.service import DeviceInfoService
from src.services.exchange_operations.services import ExchangeOperationsService
from src.services.funding_and_withdraw import FundingAndWithdrawalService
from src.services.jwt.service import JwtService


class FundingAndWithdrawalRouter:

    __funding_and_withdrawal_router = APIRouter()

    @staticmethod
    def get_user_account_router():
        return FundingAndWithdrawalRouter.__funding_and_withdrawal_router

    @staticmethod
    @__funding_and_withdrawal_router.post(
        "/user/money_flow_between_user_accounts_in_same_exchange",
        tags=["User Funding And Withdrawal"],
    )
    async def add_funding(request: Request, user_money_flow: UserMoneyFlowSameExchange):

        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        await JwtService.validate_mist(
            request=request, user_data=jwt_data["user"]
        )
        get_user_bank_accounts_response = (
            await FundingAndWithdrawalService.money_flow_between_user_dtvm_accounts(
                money_flow=user_money_flow, jwt_data=jwt_data
            )
        )

        # ADD TRANSACTION TYPE AND SPECIFY
        await ExchangeOperationsService.get_service_response_to_save_exchange_operations(
            jwt_data=jwt_data, resume=get_user_bank_accounts_response
        )

        return get_user_bank_accounts_response

    @staticmethod
    @__funding_and_withdrawal_router.post(
        "/user/money_flow_to_external_bank",
        tags=["User Funding And Withdrawal"],
    )
    async def withdrawal_to_external_bank(
        request: Request, user_withdrawal: UserMoneyFlowToExternalBank
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        await JwtService.validate_mist(
            request=request, user_data=jwt_data["user"]
        )

        jwt = ThebesAnswer(jwt_data=jwt_data)
        jwt.account_br_is_blocked()
        unique_id = jwt.unique_id

        origin_account = BrokerAccount(
            account_number=jwt.bmf_account,
            user_unique_id=unique_id,
            country=Region.BR,
        )
        await origin_account.validate_accounts_ownership()

        account_destination = BankAccount(
            bank_account_id=str(user_withdrawal.bank_account_id),
            user_unique_id=unique_id,
            country=Region.BR,
        )
        await account_destination.validate_accounts_ownership()

        device_info = await DeviceInfoService.get_device_info(request)

        get_user_bank_accounts_response = (
            await FundingAndWithdrawalService.withdrawal_to_external_bank(
                money_flow=user_withdrawal,
                jwt=jwt,
                origin_account=origin_account,
                account_destination=account_destination,
                device_info=device_info,
            )
        )

        Sindri.dict_to_primitive_types(get_user_bank_accounts_response)
        result = ResponseModel(
            result=get_user_bank_accounts_response,
            success=True,
            internal_code=InternalCode.SUCCESS,
        ).build_http_response(status_code=HTTPStatus.OK)

        await ExchangeOperationsService.get_service_response_to_save_exchange_operations(
            jwt_data=jwt_data, resume=get_user_bank_accounts_response
        )

        return result
