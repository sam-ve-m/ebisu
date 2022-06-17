from src.infrastructures.env_config import config
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class StatementsRepository(OracleBaseRepository):

    service = config("ORACLE_BASE_SERVICE_BR")
    user = config("ORACLE_BASE_USER")
    password = config("ORACLE_BASE_PASSWORD")
    base_dns = config("ORACLE_BASE_DSN")
    port = config("ORACLE_BASE_PORT")

    @staticmethod
    def list_paginated_complete_account_statement(
        offset: int,
        limit: int,
        bmf_account: str
    ):
        complete_statement_query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                    FROM CORRWIN.TCCMOVTO
                    WHERE CD_CLIENTE = {bmf_account}          
                    ORDER BY NR_LANCAMENTO
                    OFFSET {offset} rows
                    fetch first {limit} row only"""

        statement = StatementsRepository.get_data(
            sql=complete_statement_query
        )
        return statement

    @staticmethod
    def get_account_balance(bmf_account: str):
        balance_query = f"SELECT VL_TOTAL FROM CORRWIN.TCCSALREF WHERE CD_CLIENTE = {bmf_account}"
        balance = StatementsRepository.get_data(
            sql=balance_query
        )
        return balance
