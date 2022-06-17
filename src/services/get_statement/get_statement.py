from datetime import datetime

from src.domain.enums.region import Region
from src.domain.enums.statement_type import StatementType
from src.domain.statement.response.model import StatementModelToResponse, StatementResponse
from src.domain.validators.exchange_info.get_statement_validator import (
    GetStatementModel,
)
from src.repositories.statements.repository import StatementsRepository
from src.services.statement.service import Statement


class GetStatement:

    @classmethod
    async def get_service_response(cls, jwt_data: dict, statement: GetStatementModel) -> StatementResponse:
        map_keys = (statement.region, statement.statement_type)
        statement_response = {
            (Region.BR, StatementType.ALL): GetStatement.get_complete_br_statement,
            (Region.BR, StatementType.FUTURE): GetStatement.get_future_br_statement,
            (Region.BR, StatementType.OUTFLOWS): GetStatement.get_outflows_br_statement,
            (Region.BR, StatementType.INFLOWS): GetStatement.get_inflows_br_statement,
            (Region.US, StatementType.ALL): GetStatement.get_complete_us_statement,
        }.get(map_keys, {})

        statement_response = await statement_response(jwt_data=jwt_data, statement=statement)

        return statement_response

    @staticmethod
    def extract_bmf_account(jwt_data: dict) -> str:
        br_portfolios = jwt_data.get("user", {}).get("portfolios", {}).get("br", {})
        bmf_account = br_portfolios.get("bmf_account")

        return bmf_account

    @classmethod
    async def get_complete_br_statement(cls, jwt_data: dict, statement: GetStatementModel) -> StatementResponse:
        bmf_account = GetStatement.extract_bmf_account(jwt_data=jwt_data)

        balance = StatementsRepository.get_account_balance(
            bmf_account=bmf_account
        )

        transactions = StatementsRepository.list_paginated_complete_account_transactions(
            offset=statement.offset,
            limit=statement.limit,
            bmf_account=bmf_account
        )

        statement_response = StatementModelToResponse.statement_response(
            balance=balance,
            transactions=transactions
        )

        return statement_response

    @classmethod
    async def get_future_br_statement(cls, jwt_data: dict, statement: GetStatementModel):
        bmf_account = cls.extract_bmf_account(jwt_data=jwt_data)

        balance = StatementsRepository.get_account_balance(
            bmf_account=bmf_account
        )

        transactions = StatementsRepository.list_paginated_future_account_transactions(
            offset=statement.offset,
            limit=statement.limit,
            bmf_account=bmf_account
        )

        statement_response = StatementModelToResponse.statement_response(
            balance=balance,
            transactions=transactions
        )

        return statement_response

    @classmethod
    async def get_outflows_br_statement(cls, jwt_data: dict, statement: GetStatementModel):
        bmf_account = cls.extract_bmf_account(jwt_data=jwt_data)

        balance = StatementsRepository.get_account_balance(
            bmf_account=bmf_account
        )

        transactions = StatementsRepository.list_paginated_outflow_account_transactions(
            offset=statement.offset,
            limit=statement.limit,
            bmf_account=bmf_account
        )

        statement_response = StatementModelToResponse.statement_response(
            balance=balance,
            transactions=transactions
        )

        return statement_response

    @classmethod
    async def get_inflows_br_statement(cls, jwt_data: dict, statement: GetStatementModel):
        bmf_account = cls.extract_bmf_account(jwt_data=jwt_data)

        balance = StatementsRepository.get_account_balance(
            bmf_account=bmf_account
        )

        transactions = StatementsRepository.list_paginated_outflow_account_transactions(
            offset=statement.offset,
            limit=statement.limit,
            bmf_account=bmf_account
        )

        statement_response = StatementModelToResponse.statement_response(
            balance=balance,
            transactions=transactions
        )

        return statement_response

    @classmethod
    async def get_complete_us_statement(cls, jwt_data: dict, statement: GetStatementModel):

        # us_portfolios = jwt_data.get("user", {}).user.get("portfolios", {}).get("us", {})
        # dw_account = us_portfolios.get("dw_account")
        dw_account = "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006"

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
