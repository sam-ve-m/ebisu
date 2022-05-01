from fastapi import Request, APIRouter

from api.domain.validators.funding_and_withdrawal.validators import UserMoneyFlow, UserMoneyFloSameExchange, \
    UserMoneyFloDifferentExchange
from api.services.bank_account.service import UserBankAccountService
from api.services.funding_and_withdrawal.service import FundingAndWithdrawalService
from api.services.jwt.service_jwt import JwtService
from api.domain.exception.model import InvalidElectronicaSignature

class FundingAndWithdrawalRouter:

    __funding_and_withdrawal_router = APIRouter()

    @staticmethod
    def get_user_account_router():
        return FundingAndWithdrawalRouter.__funding_and_withdrawal_router

    @staticmethod
    async def get_jwt_data_and_validate_electronica_signature(request: Request):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        valid_electronica_signature = await JwtService.validate_electronic_signature(request, user_data=jwt_data["user"])
        if not valid_electronica_signature:
            raise InvalidElectronicaSignature()
        return jwt_data

    @staticmethod
    @__funding_and_withdrawal_router.post("/user/money_flow_between_user_accounts_in_same_exchange", tags=["User Funding And Withdrawal"])
    async def add_funding(request: Request, user_money_flow: UserMoneyFloSameExchange):
        jwt_data = await FundingAndWithdrawalRouter.get_jwt_data_and_validate_electronica_signature(request=request)
        money_flow_between_user_accounts_request_data = {
            "x-thebes-answer": jwt_data,
        }
        money_flow_between_user_accounts_request_data.update(user_money_flow.dict())
        get_user_bank_accounts_response = await FundingAndWithdrawalService.money_flow_between_user_dtvm_accounts(money_flow_between_user_accounts_request_data)
        return get_user_bank_accounts_response

    @staticmethod
    @__funding_and_withdrawal_router.post("/user/money_flow_between_user_accounts_between_different_exchange", tags=["User Funding And Withdrawal"])
    async def add_funding(request: Request, user_money_flow: UserMoneyFloDifferentExchange):
        jwt_data = await FundingAndWithdrawalRouter.get_jwt_data_and_validate_electronica_signature(request=request)

        money_flow_between_user_accounts_request_data = {
            "x-thebes-answer": jwt_data,
        }
        money_flow_between_user_accounts_request_data.update(user_money_flow.dict())
        get_user_bank_accounts_response = await FundingAndWithdrawalService.money_flow_between_user_dtvm_accounts(
            money_flow_between_user_accounts_request_data)
        return get_user_bank_accounts_response
