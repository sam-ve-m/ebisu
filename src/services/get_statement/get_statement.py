from datetime import datetime

from src.domain.enums.statement_type import StatementType
from src.domain.statement.br.response.model import StatementModelToResponse, StatementResponse
from src.domain.statement.us.request.model import TransactionRequest
from src.domain.validators.exchange_info.get_statement_validator import (
    GetBrStatementModel, GetUsStatementModel,
)
from src.repositories.statements.repository import StatementsRepository
from src.repositories.user_portfolios.repository import UserPortfoliosRepository
from src.services.statement.service import Statement
from src.transport.drive_wealth.statement.transport import DwStatementTransport


class GetStatement:

    @staticmethod
    def __extract_bmf_account(jwt_data: dict) -> str:
        br_portfolios = jwt_data.get("user", {}).get("portfolios", {}).get("br", {})
        bmf_account = br_portfolios.get("bmf_account")

        return bmf_account

    @classmethod
    async def get_br_bank_statement(cls, jwt_data: dict, statement: GetBrStatementModel) -> StatementResponse:

        list_statement_repository = {
            StatementType.ALL: StatementsRepository.list_paginated_complete_account_transactions,
            StatementType.FUTURE: StatementsRepository.list_paginated_future_account_transactions,
            StatementType.OUTFLOWS: StatementsRepository.list_paginated_outflow_account_transactions,
            StatementType.INFLOWS: StatementsRepository.list_paginated_inflow_account_transactions,
        }.get(statement.statement_type)

        bmf_account = GetStatement.__extract_bmf_account(jwt_data=jwt_data)

        balance = StatementsRepository.get_account_balance(
            bmf_account=bmf_account
        )

        transactions = list_statement_repository(
            offset=statement.offset,
            limit=statement.limit,
            bmf_account=bmf_account
        )

        statement_response = StatementModelToResponse.statement_response(
            balance=balance,
            transactions=transactions
        )

        return statement_response

    @staticmethod
    def __extract_identifier_data_from_jwt(jwt_data: dict) -> str:
        user = jwt_data.get("user", {})
        dw_account = user.get("portfolios", {}).get("us", {}).get("dw_account")

        unique_id = user.get("unique_id")

        return unique_id, dw_account

    @staticmethod
    async def __get_range_date_bank_statement(unique_id: str, requested_offset: int):
        from_date = await UserPortfoliosRepository.get_default_portfolio_created_at_by_region(
            unique_id=unique_id,
            region="US"
        )

        to_date = datetime.now().timestamp() * 1000

        if requested_offset is None:
            requested_offset = from_date

        return from_date, to_date, requested_offset

    @staticmethod
    async def get_us_bank_statement(jwt_data: dict, statement: GetUsStatementModel):
        unique_id, dw_account = GetStatement.__extract_identifier_data_from_jwt(
            jwt_data=jwt_data
        )

        from_date, to_date, offset = await GetStatement.__get_range_date_bank_statement(
            unique_id=unique_id,
            requested_offset=statement.offset
        )

        us_statement = await Statement.get_dw_statement(
            dw_account=dw_account,
            from_date=from_date,
            to_date=to_date,
            offset=offset,
            limit=statement.limit,
        )

        statements = us_statement.get("statements")

        last_transaction = statements[-1]

        date = last_transaction.get("date")

        us_statement.update({"offset": date})

        # if not us_statement:
        #     return {}

        return us_statement

    @staticmethod
    async def get_dw_statement(
        transaction_request: TransactionRequest
    ) -> dict:

        raw_transactions = await DwStatementTransport.get_transactions(
            dw_account, limit=limit, offset=offset_date, from_date=from_date, to_date=to_date
        )
        raw_balance = await DwStatementTransport.get_balances(dw_account)
        # TODO INTERNAL SERVER ERROR
        balance = Statement.normalize_balance_us(*raw_balance)
        statement = Statement.normalize_statement_us(*raw_transactions)
        return {"balance": balance, "statements": statement}
