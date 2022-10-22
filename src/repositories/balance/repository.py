from etria_logger import Gladsheim

from src.domain.balance.br.model import Balance
from src.infrastructures.env_config import config
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class BalanceRepository(OracleBaseRepository):

    service = config("ORACLE_BASE_SERVICE_BR")
    user = config("ORACLE_BASE_USER")
    password = config("ORACLE_BASE_PASSWORD")
    base_dns = config("ORACLE_BASE_DSN")
    port = config("ORACLE_BASE_PORT")

    @staticmethod
    async def get_balance(account: str) -> Balance:

        query = f"""SELECT NVL(VL_TOTAL,0) as VL_TOTAL, NVL(VL_DISPONIVEL, 0) as VL_DISPONIVEL FROM CORRWIN.TCCSALREF A 
            WHERE DT_REFERENCIA = (SELECT max(DT_REFERENCIA) from CORRWIN.TCCSALREF where CD_CLIENTE = A.CD_CLIENTE) 
            AND CD_CLIENTE = {account}"""

        try:
            balance = BalanceRepository.fetch_one(sql=query)

            balance = balance if balance else {}

            balance = Balance(
                available_for_trade=balance.get("VL_TOTAL", 0),
                available_for_withdraw=balance.get("VL_DISPONIVEL", 0),
            )
            return balance

        except Exception as ex:
            Gladsheim.error(
                message=f"GetBrBalance::get_balance::Error to get balance in BR",
                account=account,
                error=ex,
            )
            raise ex
