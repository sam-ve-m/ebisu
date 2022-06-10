from src.domain.enums.region import Region
from src.domain.enums.statement_type import StatementType
from src.domain.validators.exchange_info.get_statement_validator import (
    GetStatementModel,
)
from src.repositories.statements.repository import StatementsRepository
from src.services.statement.service import Statement


class GetStatement:
    oracle_singleton_instance = StatementsRepository

    @classmethod
    def get_all_br_statement(cls, jwt_data: dict, statement: GetStatementModel):

        br_portfolios = jwt_data.get("user", {}).user.get("portfolios", {}).get("br", {})
        bmf_account = br_portfolios.get("bmf_account")

        statement = StatementsRepository.build_query_all_br(
            bmf_account=bmf_account,
            offset=statement.offset,
            limit=statement.limit
        )

        balance = StatementsRepository.build_query_statement_client(bmf_account=bmf_account)

        data_balance = {
            "balance": balance.pop().get("VL_TOTAL"),
            "statements": [
                Statement.normalize_statement(transc) for transc in statement
            ],}

        if not data_balance:
            return {}

        return data_balance

    @classmethod
    async def get_future_br_statement(cls, jwt_data: dict, statement: GetStatementModel):
        br_portfolios = jwt_data.get("user", {}).user.get("portfolios", {}).get("br", {})
        bmf_account = br_portfolios.get("bmf_account")

        future_statement = StatementsRepository.build_query_future(
            bmf_account=bmf_account,
            offset=statement.offset,
            limit=statement.limit
        )

        balance = StatementsRepository.build_query_statement_client(bmf_account=bmf_account)

        data_balance = {
            "balance": balance.pop().get("VL_TOTAL"),
            "statements": [
                Statement.normalize_statement(transc) for transc in future_statement
            ], }

        if not data_balance:
            return {}

        return data_balance


    @classmethod
    async def get_all_us_statement(cls, jwt_data: dict, statement: GetStatementModel):

        us_portfolios = jwt_data.get("user", {}).user.get("portfolios", {}).get("us", {})
        dw_account = us_portfolios.get("dw_account")

        us_statement = await Statement.get_dw_statement(
            dw_account=dw_account,
            offset=statement.offset,
            limit=statement.limit
        )
        if not us_statement:
            return {}

        return us_statement

    @classmethod
    def get_service_response(cls, jwt_data: dict, statement: GetStatementModel) -> dict:

        map_keys = (statement.region, statement.statement_type)

        statement_response = {
            (Region.BR, StatementType.ALL) : GetStatement.get_all_br_statement,
            (Region.BR, StatementType.FUTURE): GetStatement.get_future_br_statement,
            (Region.US, StatementType.ALL): GetStatement.get_all_us_statement,
        }.get(map_keys, {})(jwt_data=jwt_data, statement=statement)

        return statement_response
