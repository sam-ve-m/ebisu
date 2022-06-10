from src.infrastructures.env_config import config
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class StatementsRepository(OracleBaseRepository):
    service = config("ORACLE_BASE_SERVICE_BR")
    user = config("ORACLE_BASE_USER")
    password = config("ORACLE_BASE_PASSWORD")
    base_dns = config("ORACLE_BASE_DSN")
    port = config("ORACLE_BASE_PORT")

    @staticmethod
    def build_query_statement(
            bmf_account: str,
            start_date,
            end_date,
            offset: int,
            limit: int
    ):
        query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                           FROM CORRWIN.TCCMOVTO 
                           WHERE CD_CLIENTE = {bmf_account} 
                           AND DT_LANCAMENTO >= TO_DATE('{start_date}', 'yyyy-MM-dd')
                           AND DT_LANCAMENTO <= TO_DATE('{end_date}', 'yyyy-MM-dd')                   
                           ORDER BY NR_LANCAMENTO
                           OFFSET {offset} rows
                           fetch first {limit} row only
                           """
        return query

    @staticmethod
    def build_query_statement_client(
            bmf_account: str
    ):
        query = (
            f"SELECT VL_TOTAL FROM CORRWIN.TCCSALREF WHERE CD_CLIENTE = {bmf_account}"
        )

        return query
