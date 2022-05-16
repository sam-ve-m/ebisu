from src.domain.enums.region import Region
from src.domain.validators.exchange_info.get_statement_validator import (
    GetStatementModel,
)
from src.repositories.statements.repository import StatementsRepository
from src.services.statement.service import Statement


class GetStatement:
    oracle_singleton_instance = StatementsRepository

    @classmethod
    async def get_service_response(
        cls, jwt_data: dict, statement: GetStatementModel
    ) -> dict:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        us_portfolios = portfolios.get("us", {})

        dw_account = us_portfolios.get("dw_account")
        bmf_account = br_portfolios.get("bmf_account")

        if statement.region == Region.US:
            us_statement = await Statement.get_dw_statement(
                dw_account=dw_account,
                start_date=statement.start_date,
                end_date=statement.end_date,
                offset=statement.offset,
                limit=statement.limit,
            )
            return us_statement

        start_date = Statement.from_timestamp_to_utc_isoformat_br(statement.start_date)
        end_date = Statement.from_timestamp_to_utc_isoformat_br(statement.end_date)
        query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM CORRWIN.TCCMOVTO 
                   WHERE CD_CLIENTE = {bmf_account} 
                   AND DT_LANCAMENTO >= TO_DATE('{start_date}', 'yyyy-MM-dd')
                   AND DT_LANCAMENTO <= TO_DATE('{end_date}', 'yyyy-MM-dd')                   
                   ORDER BY NR_LANCAMENTO
                   OFFSET {statement.offset} rows
                   fetch first {statement.limit} row only
                   """
        statement = GetStatement.oracle_singleton_instance.get_data(sql=query)
        query = (
            f"SELECT VL_TOTAL FROM CORRWIN.TCCSALREF WHERE CD_CLIENTE = {bmf_account}"
        )
        balance = GetStatement.oracle_singleton_instance.get_data(sql=query)

        data_balance = {
            "balance": balance.pop().get("VL_TOTAL"),
            "statements": [
                Statement.normalize_statement(transc) for transc in statement
            ],
        }
        if not data_balance:
            return {}

        return data_balance
