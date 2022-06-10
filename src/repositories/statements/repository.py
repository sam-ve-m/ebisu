from src.infrastructures.env_config import config
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class StatementsRepository(OracleBaseRepository):

    service = config("ORACLE_BASE_SERVICE_BR")
    user = config("ORACLE_BASE_USER")
    password = config("ORACLE_BASE_PASSWORD")
    base_dns = config("ORACLE_BASE_DSN")
    port = config("ORACLE_BASE_PORT")

    @staticmethod
    def build_query_all_br(
            bmf_account: str,
            offset: int,
            limit: int
    ):
        query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM CORRWIN.TCCMOVTO 
                   WHERE CD_CLIENTE = {bmf_account}                 
                   ORDER BY NR_LANCAMENTO
                   OFFSET {offset} rows
                   fetch first {limit} row only
                """

        statement = StatementsRepository.get_data(sql=query)

        return statement

    @staticmethod
    def build_query_statement_client(
            bmf_account: str
    ):
        query = (
            f"SELECT VL_TOTAL FROM CORRWIN.TCCSALREF WHERE CD_CLIENTE = {bmf_account}"
        )

        balance = StatementsRepository.get_data(sql=query)

        return balance

    @staticmethod
    def build_query_future(
            bmf_account: str,
            offset: int,
            limit: int
    ):
        query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM CORRWIN.TCCMOVTO 
                   WHERE CD_CLIENTE = {bmf_account} AND
                   DT_LANCAMENTO > sysdate + 1                 
                   ORDER BY NR_LANCAMENTO
                   OFFSET {offset} rows
                   fetch first {limit} row only
                """

        statement_future = StatementsRepository.get_data(sql=query)
        return statement_future
