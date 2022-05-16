# External Libs
from src.repositories.earnings.repository import EarningsClientRepository


class GetBrEarningsDetails:

    oracle_earnings_client_singleton_instance = EarningsClientRepository

    @staticmethod
    def build_query_payable_earnings(cod_client: int, limit: int, offset: int) -> str:
        # query to find the earnings of a specific client but not including the date 31-12-9999

        query = f"""
                SELECT MA.COD_CLI, MA.DESC_HIST_MVTO, TM.DESC_RESU_TIPO_MVTO, 
                MA.COD_NEG, MA.QTDE_MVTO, MA.PREC_LQDO, MA.DATA_MVTO                
                FROM CORRWIN.TCFMOVI_ACAO MA
                LEFT JOIN CORRWIN.TCFTIPO_MVTO TM ON TM.cod_tipo_mvto= MA.tipo_mvto
                WHERE COD_CLI = ('{cod_client}') 
                AND DATA_MVTO >= sysdate + 1 
                AND DATA_MVTO <> TO_DATE('31-DEC-9999', 'DD-MM-YYYY')
                OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
                """
        return query

    @staticmethod
    def build_query_record_date_earnings(
        cod_client: int, limit: int, offset: int
    ) -> str:
        # query to find record date == 31-12-9999 (to be paid with no date specified)

        query = f"""
                SELECT MA.COD_CLI, MA.DESC_HIST_MVTO, TM.DESC_RESU_TIPO_MVTO, 
                MA.COD_NEG, MA.QTDE_MVTO, MA.PREC_LQDO, MA.DATA_MVTO                
                FROM CORRWIN.TCFMOVI_ACAO MA
                LEFT JOIN CORRWIN.TCFTIPO_MVTO TM ON TM.cod_tipo_mvto= MA.tipo_mvto
                WHERE COD_CLI = ('{cod_client}') AND DATA_MVTO = TO_DATE('31-DEC-9999', 'DD-MM-YYYY')
                OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
        """

        return query
