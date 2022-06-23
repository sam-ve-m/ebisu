from fastapi import Request, APIRouter

from src.domain.validators.funding_and_withdrawal.validators import (
    UserMoneyFlowSameExchange,
    UserMoneyFlowDifferentExchange, UserMoneyFlowToExternalBank,
)
from src.services.exchange_operations.services import ExchangeOperationsService
from src.services.funding_and_withdrawal import FundingAndWithdrawalService
from src.services.jwt.service_jwt import JwtService
from src.domain.exception.model import InvalidElectronicaSignature


class FundingAndWithdrawalRouter:

    __funding_and_withdrawal_router = APIRouter()

    @staticmethod
    def get_user_account_router():

        return FundingAndWithdrawalRouter.__funding_and_withdrawal_router

    @staticmethod
    async def get_jwt_data_and_validate_electronica_signature(request: Request):

        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        valid_electronica_signature = await JwtService.validate_electronic_signature(
            request, user_data=jwt_data["user"]
        )
        if not valid_electronica_signature:
            raise InvalidElectronicaSignature()
        return jwt_data

    @staticmethod
    @__funding_and_withdrawal_router.post(
        "/user/money_flow_between_user_accounts_in_same_exchange",
        tags=["User Funding And Withdrawal"],
    )
    async def add_funding(request: Request, user_money_flow: UserMoneyFlowSameExchange):

        jwt_data = await FundingAndWithdrawalRouter.get_jwt_data_and_validate_electronica_signature(
            request=request
        )
        get_user_bank_accounts_response = (
            await FundingAndWithdrawalService.money_flow_between_user_dtvm_accounts(
                money_flow=user_money_flow,
                jwt_data=jwt_data
            )
        )

        # ADD TRANSACTION TYPE AND SPECIFY
        await ExchangeOperationsService.get_service_response_to_save_exchange_operations(
            jwt_data=jwt_data,
            resume=get_user_bank_accounts_response)

        return get_user_bank_accounts_response

    @staticmethod
    @__funding_and_withdrawal_router.post(
        "/user/money_flow_between_user_accounts_between_different_exchange",
        tags=["User Funding And Withdrawal"],
    )
    async def add_funding(
        request: Request, user_money_flow: UserMoneyFlowDifferentExchange
    ):

        jwt_data = await FundingAndWithdrawalRouter.get_jwt_data_and_validate_electronica_signature(
            request=request
        )
        get_user_bank_accounts_response = (
            await FundingAndWithdrawalService.money_flow_between_user_dtvm_accounts(
                money_flow=user_money_flow,
                jwt_data=jwt_data
            )
        )

        # ADD TRANSACTION TYPE AND SPECIFY
        await ExchangeOperationsService.get_service_response_to_save_exchange_operations(
            jwt_data=jwt_data,
            resume=get_user_bank_accounts_response)

        return get_user_bank_accounts_response


    @staticmethod
    @__funding_and_withdrawal_router.post(
        "/user/money_flow_to_external_bank",
        tags=["User Funding And Withdrawal"],
    )
    async def withdrawal_to_external_bank(
        request: Request, user_withdrawal: UserMoneyFlowToExternalBank
    ):

        jwt_data = await FundingAndWithdrawalRouter.get_jwt_data_and_validate_electronica_signature(
            request=request
        )
        get_user_bank_accounts_response = (
            await FundingAndWithdrawalService.withdrawal_to_external_bank(
                money_flow=user_withdrawal,
                jwt_data=jwt_data
            )
        )

        # ADD TRANSACTION TYPE AND SPECIFY
        await ExchangeOperationsService.get_service_response_to_save_exchange_operations(
            jwt_data=jwt_data,
            resume=get_user_bank_accounts_response)

        return get_user_bank_accounts_response