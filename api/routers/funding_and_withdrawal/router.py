from fastapi import Request, APIRouter

from api.domain.validators.funding_and_withdrawal.validators import UserMoneyFlow
from api.services.bank_account.service import UserBankAccountService
from api.services.jwt.service_jwt import JwtService


class FundingAndWithdrawalRouter:

    __funding_and_withdrawal_router = APIRouter()

    @staticmethod
    def get_user_account_router():
        return FundingAndWithdrawalRouter.__funding_and_withdrawal_router

    @staticmethod
    @__funding_and_withdrawal_router.post("/user/money_flow_between_user_accounts_in_same_exchange", tags=["User Funding And Withdrawal"])
    async def add_funding(request: Request, user_money_flow: UserMoneyFlow):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        money_flow_between_user_accounts_request_data = {
            "x-thebes-answer": jwt_data,
        }
        money_flow_between_user_accounts_request_data.update(user_money_flow.dict())
        get_user_bank_accounts_response = await UserBankAccountService.get_user_bank_accounts(jwt_data)
        return get_user_bank_accounts_response

    @staticmethod
    @__funding_and_withdrawal_router.post("/user/money_flow_between_user_accounts_between_different_exchange", tags=["User Funding And Withdrawal"])
    async def add_funding(request: Request, user_money_flow: UserMoneyFlow):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        money_flow_between_user_accounts_request_data = {
            "x-thebes-answer": jwt_data,
        }
        money_flow_between_user_accounts_request_data.update(user_money_flow.dict())
        get_user_bank_accounts_response = await UserBankAccountService.get_user_bank_accounts(jwt_data)
        return get_user_bank_accounts_response
