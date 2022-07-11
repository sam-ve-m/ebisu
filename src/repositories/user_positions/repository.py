from typing import List

from etria_logger import Gladsheim

from src.domain.positions.model import Position
from src.infrastructures.env_config import config
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class UserPositionsRepository(OracleBaseRepository):
    service = config("ORACLE_POSITION_SERVICE")
    user = config("ORACLE_POSITION_USER")
    password = config("ORACLE_POSITION_PASSWORD")
    base_dns = config("ORACLE_POSITION_DSN")
    port = config("ORACLE_POSITION_PORT")

    @staticmethod
    def __build_query_br(account: str) -> str:
        query = f"""
                SELECT
                A.COD_NEG AS SYMBOL,
                A.QTDE_TOT AS QUANTITY
                FROM CORRWIN.VCFPOSICAO A
                JOIN CORRWIN.TCFPAP_MERC B ON A.NUM_DIST = B.NUM_DIST AND A.TIPO_MERC = B.TIPO_MERC AND A.COD_NEG = B.COD_NEG
                WHERE A.COD_CLI = {account} AND  A.QTDE_TOT != 0    
                """

        return query

    @classmethod
    async def get_positions(cls, account: str) -> List[Position]:
        try:
            query = cls.__build_query_br(account)
            raw_positions = cls.get_data(query)
            positions = []

            for position in raw_positions:
                symbol = position.get('SYMBOL')
                quantity = position.get('QUANTITY')
                positions.append(Position(symbol=symbol, quantity=quantity))
            return positions

        except Exception as ex:
            message = "Failed to get positions"
            Gladsheim.error(error=ex, message=message, accounts=account)
            raise ex
