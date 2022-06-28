from datetime import datetime

from src.domain.enums.region import Region
from src.domain.enums.statement_type import StatementType
from src.domain.statement.response.model import (
    StatementModelToResponse,
    StatementResponse,
)
from src.domain.validators.exchange_info.get_statement_validator import (
    GetBrStatementModel,
)
from src.repositories.statements.repository import StatementsRepository
from src.services.statement.service import Statement


class GetStatement:
    @staticmethod
    def __extract_bmf_account(jwt_data: dict) -> str:
        br_portfolios = jwt_data.get("user", {}).get("portfolios", {}).get("br", {})
        bmf_account = br_portfolios.get("bmf_account")

        return bmf_account

    @classmethod
    async def get_br_bank_statement(
        cls, jwt_data: dict, statement: GetBrStatementModel
    ) -> StatementResponse:

        list_statement_repository = {
            StatementType.ALL: StatementsRepository.list_paginated_complete_account_transactions,
            StatementType.FUTURE: StatementsRepository.list_paginated_future_account_transactions,
            StatementType.OUTFLOWS: StatementsRepository.list_paginated_outflow_account_transactions,
            StatementType.INFLOWS: StatementsRepository.list_paginated_inflow_account_transactions,
        }.get(statement.statement_type)

        bmf_account = GetStatement.__extract_bmf_account(jwt_data=jwt_data)

        balance = StatementsRepository.get_account_balance(bmf_account=bmf_account)

        transactions = list_statement_repository(
            offset=statement.offset, limit=statement.limit, bmf_account=bmf_account
        )

        statement_response = StatementModelToResponse.statement_response(
            balance=balance, transactions=transactions
        )

        return statement_response

    @staticmethod
    def __extract_dw_account(jwt_data: dict) -> str:
        # us_portfolios = jwt_data.get("user", {}).user.get("portfolios", {}).get("us", {})
        # dw_account = us_portfolios.get("dw_account")
        dw_account = "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006"

        return dw_account

    @classmethod
    async def get_us_bank_statement(
        cls, jwt_data: dict, statement: GetBrStatementModel
    ):
        dw_account = GetStatement.__extract_dw_account(jwt_data=jwt_data)

        # TODO: Pegar do Mongo DB
        start_date = 1609542250000
        end_date = datetime.now().timestamp() * 1000

        us_statement = await Statement.get_dw_statement(
            dw_account=dw_account,
            offset=statement.offset,
            limit=statement.limit,
            start_date=start_date,
            end_date=end_date,
        )

        if not us_statement:
            return {}

        return us_statement
