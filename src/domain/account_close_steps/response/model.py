from typing import List
import functools

from pydantic import BaseModel

from src.domain.account_close_steps.model import AccountCloseSteps


class AccountSteps(BaseModel):
    balance: bool
    positions: bool
    earnings: bool
    region: str
    type: str = "default"


class AccountCloseStepsResponse(BaseModel):
    has_permission_to_close_account: bool
    accounts_steps: List[AccountSteps]


class AccountCloseStepsToResponse:
    @staticmethod
    def account_close_steps_response(
        accounts_close_steps: List[AccountCloseSteps],
    ) -> AccountCloseStepsResponse:
        has_permission_to_close_account = True
        accounts_steps: List[AccountSteps] = []
        for account_close_steps in accounts_close_steps:
            has_permission_to_close_account = (
                has_permission_to_close_account
                and account_close_steps.has_permission_to_close_account()
            )
            account_steps = account_close_steps.get_account_steps()
            account_steps = AccountSteps(**account_steps)
            accounts_steps.append(account_steps)

        account_close_steps_response = {
            "has_permission_to_close_account": has_permission_to_close_account,
            "accounts_steps": accounts_steps,
        }

        result = AccountCloseStepsResponse(**account_close_steps_response)
        return result
