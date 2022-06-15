from datetime import datetime

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
    async def get_account(cls, jwt_data: dict):
        br_portfolios = jwt_data.get("user", {}).get("portfolios", {}).get("br", {})
        bmf_account = br_portfolios.get("bmf_account")

        return bmf_account

    @classmethod
    async def get_complete_br_statement(cls, jwt_data: dict, statement: GetStatementModel):
        bmf_account = cls.get_account(jwt_data=jwt_data)

        # todo - retirar futuros
        additional_clause = f""" WHERE CD_CLIENTE = {bmf_account} """

        complete_statement = StatementsRepository.build_general_query(
            offset=statement.offset,
            limit=statement.limit,
            additional_clause=additional_clause
        )

        balance = StatementsRepository.build_query_balance(bmf_account=bmf_account)

        data_balance = {
            "balance": balance.pop().get("VL_TOTAL"),
            "statements": [
                Statement.normalize_statement(transc) for transc in complete_statement
            ],}

        if not data_balance:
            return {}

        return data_balance

    @classmethod
    async def get_future_br_statement(cls, jwt_data: dict, statement: GetStatementModel):
        bmf_account = cls.get_account(jwt_data=jwt_data)

        additional_clause = f"""WHERE CD_CLIENTE = {bmf_account} AND DT_LANCAMENTO > sysdate + 1"""

        future_statement = StatementsRepository.build_general_query(
            offset=statement.offset,
            limit=statement.limit,
            additional_clause=additional_clause
        )

        data_balance = {
            "statements": [
                Statement.normalize_statement(transc) for transc in future_statement
            ], }

        if not data_balance:
            return {}

        return data_balance

    @classmethod
    async def get_outflows_br_statement(cls, jwt_data: dict, statement: GetStatementModel):
        bmf_account = cls.get_account(jwt_data=jwt_data)

        additional_clause = f""" WHERE CD_CLIENTE = {bmf_account} AND VL_LANCAMENTO < 0 """

        outflows_statement = StatementsRepository.build_general_query(
            offset=statement.offset,
            limit=statement.limit,
            additional_clause=additional_clause
        )

        data_balance = {
            "statements": [
                Statement.normalize_statement(transc) for transc in outflows_statement
            ], }

        if not data_balance:
            return {}

        return data_balance

    @classmethod
    async def get_inflows_br_statement(cls, jwt_data: dict, statement: GetStatementModel):
        bmf_account = cls.get_account(jwt_data=jwt_data)

        additional_clause = f""" WHERE CD_CLIENTE = {bmf_account} AND VL_LANCAMENTO > 0 """

        inflows_statement = StatementsRepository.build_general_query(
            offset=statement.offset,
            limit=statement.limit,
            additional_clause=additional_clause
        )

        data_balance = {
            "statements": [
                Statement.normalize_statement(transc) for transc in inflows_statement
            ], }

        if not data_balance:
            return {}

        return data_balance

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

    @classmethod
    async def get_service_response(cls, jwt_data: dict, statement: GetStatementModel) -> dict:

        map_keys = (statement.region, statement.statement_type)

        statement_response = {
            (Region.BR, StatementType.ALL) : GetStatement.get_complete_br_statement,
            (Region.BR, StatementType.FUTURE): GetStatement.get_future_br_statement,
            (Region.BR, StatementType.OUTFLOWS): GetStatement.get_outflows_br_statement,
            (Region.BR, StatementType.INFLOWS): GetStatement.get_inflows_br_statement,
            (Region.US, StatementType.ALL): GetStatement.get_complete_us_statement,
        }.get(map_keys, {})(jwt_data=jwt_data, statement=statement)

        return await statement_response
    #
    # (Region.US, StatementType.FUTURE): GetStatement.get_future_us_statement,
    # (Region.US, StatementType.OUTFLOWS): GetStatement.get_outflows_us_statement,
    # (Region.US, StatementType.INFLOWS): GetStatement.get_inflows_us_statement
