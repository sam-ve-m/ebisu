# STANDARD LIBS
from typing import List

# PROJECT IMPORTS
from src.domain.enums.earnings_types import EarningsTypes
from src.repositories.earnings.repository import EarningsClientRepository


class GetBrEarningsDetails:

    oracle_earnings_client_singleton_instance = EarningsClientRepository

    @staticmethod
    def build_query_payable_earnings(
        cod_client: int,
        limit: int,
        offset: int,
        earnings_types: List[EarningsTypes] = None,
    ) -> str:
        # query to find the earnings of a specific client but not including the date 31-12-9999
        earnings_types_where_clause = (
            GetBrEarningsDetails.build_earnings_types_where_clause(earnings_types)
        )

        query = f"""
            SELECT MA.COD_CLI, MA.DESC_HIST_MVTO, TM.DESC_RESU_TIPO_MVTO, 
            MA.COD_NEG, MA.QTDE_MVTO, MA.PREC_LQDO, MA.DATA_MVTO                
            FROM CORRWIN.TCFMOVI_ACAO MA
            LEFT JOIN CORRWIN.TCFTIPO_MVTO TM ON TM.cod_tipo_mvto= MA.tipo_mvto
            WHERE COD_CLI = ('{cod_client}') 
            {earnings_types_where_clause}
            AND DATA_MVTO <> TO_DATE('31-DEC-9999', 'DD-MM-YYYY')
            AND DATA_MVTO >= sysdate + 1
            OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
        """
        return query

    @staticmethod
    def build_query_paid_earnings(
            cod_client: int,
            limit: int,
            offset: int,
            earnings_types: List[EarningsTypes] = None
    ) -> str:
        # query to find all already paid earnings
        earnings_types_where_clause = (
            GetBrEarningsDetails.build_earnings_types_where_clause(earnings_types)
        )
        query = f"""
                    SELECT MA.COD_CLI, MA.DESC_HIST_MVTO, TM.DESC_RESU_TIPO_MVTO, 
                    MA.COD_NEG, MA.QTDE_MVTO, MA.PREC_LQDO, MA.DATA_MVTO                
                    FROM CORRWIN.TCFMOVI_ACAO MA
                    LEFT JOIN CORRWIN.TCFTIPO_MVTO TM ON TM.cod_tipo_mvto= MA.tipo_mvto
                    WHERE COD_CLI = ('{cod_client}') 
                    {earnings_types_where_clause}
                    AND DATA_MVTO <> TO_DATE('31-DEC-9999', 'DD-MM-YYYY')
                    AND DATA_MVTO <= sysdate 
                    OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
                """
        return query

    @staticmethod
    def build_query_record_date_earnings(
        cod_client: int,
        limit: int,
        offset: int,
        earnings_types: List[EarningsTypes] = None,
    ) -> str:
        # query to find record date == 31-12-9999 (to be paid with no date specified)

        earnings_types_where_clause = (
            GetBrEarningsDetails.build_earnings_types_where_clause(earnings_types)
        )

        query = f"""
            SELECT MA.COD_CLI, MA.DESC_HIST_MVTO, TM.DESC_RESU_TIPO_MVTO, 
            MA.COD_NEG, MA.QTDE_MVTO, MA.PREC_LQDO, MA.DATA_MVTO                
            FROM CORRWIN.TCFMOVI_ACAO MA
            LEFT JOIN CORRWIN.TCFTIPO_MVTO TM ON TM.cod_tipo_mvto= MA.tipo_mvto
            WHERE COD_CLI = ('{cod_client}') 
            {earnings_types_where_clause}
            AND DATA_MVTO = TO_DATE('31-DEC-9999', 'DD-MM-YYYY')
            OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
        """

        return query

    @staticmethod
    def build_earnings_types_where_clause(earnings_types: List[EarningsTypes]):
        earnings_types_where_clause = ""
        if earnings_types:
            earnings_types_normalized = [
                earnings_type.value for earnings_type in earnings_types
            ]
            earnings_types_where_clause = (
                f"""AND MA.TIPO_MVTO in ('{"','".join(earnings_types_normalized)}')"""
            )
        return earnings_types_where_clause

    @staticmethod
    def normalize_earnings_data(client_earnings: dict) -> dict:
        normalized_data = {
            "symbol": client_earnings.get("COD_CLI"),
            "trade_history": client_earnings.get("DESC_HIST_MVTO"),
            "trade_type": client_earnings.get("DESC_RESU_TIPO_MOVTO"),
            "trade_code": client_earnings.get("COD_NEG"),
            "transaction_amount": client_earnings.get("QTDE_MVTO"),
            "net_price": client_earnings.get("PREC_LQDO"),
            "transaction_date": client_earnings.get("DATA_MVTO"),
        }

        return normalized_data
