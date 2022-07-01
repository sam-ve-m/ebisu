# STANDARD IMPORTS
from typing import List

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.earning.br.model import EarningBr
from src.infrastructures.env_config import config
from src.domain.enums.earnings_types import EarningsTypes
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class EarningsClientRepository(OracleBaseRepository):
    service = config("ORACLE_BASE_SERVICE_BR")
    user = config("ORACLE_BASE_USER")
    password = config("ORACLE_BASE_PASSWORD")
    base_dns = config("ORACLE_BASE_DSN")
    port = config("ORACLE_BASE_PORT")


class EarningsBrRecord:
    oracle_earnings_client_singleton_instance = EarningsClientRepository

    @staticmethod
    def build_br_earning_model(earning_transaction: dict) -> EarningBr:
        earning_model = EarningBr(
            symbol=earning_transaction.get("COD_NEG"),
            description=earning_transaction.get("DESC_HIST_MVTO", "NOT INFORMED"),
            amount_per_share=earning_transaction.get("AMOUNT_PER_SHARE"),
            share_quantity=earning_transaction.get("QTDE_MVTO"),
            date=RegionStringDateTime(
                date=earning_transaction.get("DATA_MVTO"),
                region_date_format=RegionDateFormat.BR_DATE_FORMAT
            ))

        return earning_model

    @staticmethod
    def get_br_payable_earnings(
            account: str,
            limit: int,
            earnings_types: List[EarningsTypes] = None,
    ) -> list:
        # query to find the earning of a specific client but not including the date 31-12-9999
        earnings_types_where_clause = (
            EarningsBrRecord.build_earnings_types_where_clause(earnings_types)
        )

        query = f"""
            SELECT MA.DESC_HIST_MVTO, MA.COD_NEG, MA.QTDE_MVTO, MA.PREC_LQDO/MA.QTDE_MVTO AS AMOUNT_PER_SHARE, 
            MA.PREC_LQDO, MA.DATA_MVTO                
            FROM CORRWIN.TCFMOVI_ACAO MA
            LEFT JOIN CORRWIN.TCFTIPO_MVTO TM ON TM.cod_tipo_mvto= MA.tipo_mvto
            WHERE COD_CLI = ('{account}') 
            {earnings_types_where_clause}
            AND DATA_MVTO <> TO_DATE('31-DEC-9999', 'DD-MM-YYYY')
            AND DATA_MVTO >= sysdate + 1
            AND MA.COD_NEG IS NOT NULL
            AND MA.QTDE_MVTO IS NOT NULL
           	AND MA.DATA_MVTO IS NOT NULL
            FETCH NEXT {limit} ROWS ONLY
        """
        payable_earnings_transactions = (
            EarningsClientRepository.get_data(
                sql=query
            )
        )

        earning_model = [
            EarningsBrRecord.build_br_earning_model(earning_transaction=earning_transaction)
            for earning_transaction in payable_earnings_transactions if earning_transaction.get("AMOUNT_PER_SHARE")
        ]
        return earning_model

    @staticmethod
    def get_br_paid_earnings(
            account: str,
            limit: int,
            earnings_types: List[EarningsTypes] = None
    ) -> list:
        # query to find all already paid earning
        earnings_types_where_clause = (
            EarningsBrRecord.build_earnings_types_where_clause(earnings_types)
        )
        query = f"""
                    SELECT MA.DESC_HIST_MVTO, MA.COD_NEG, MA.QTDE_MVTO, MA.PREC_LQDO/MA.QTDE_MVTO AS AMOUNT_PER_SHARE, 
                    MA.PREC_LQDO, MA.DATA_MVTO                
                    FROM CORRWIN.TCFMOVI_ACAO MA
                    LEFT JOIN CORRWIN.TCFTIPO_MVTO TM ON TM.cod_tipo_mvto= MA.tipo_mvto
                    WHERE COD_CLI = ('{account}') 
                    {earnings_types_where_clause}
                    AND DATA_MVTO <> TO_DATE('31-DEC-9999', 'DD-MM-YYYY')
                    AND DATA_MVTO <= sysdate
                    AND MA.COD_NEG IS NOT NULL
                    AND MA.QTDE_MVTO IS NOT NULL
                    AND MA.DATA_MVTO IS NOT NULL
                    FETCH NEXT {limit} ROWS ONLY
                """

        paid_earnings_transactions = (
            EarningsClientRepository.get_data(
                sql=query
            )
        )

        earning_model = [
            EarningsBrRecord.build_br_earning_model(earning_transaction=earning_transaction)
            for earning_transaction in paid_earnings_transactions if earning_transaction.get("AMOUNT_PER_SHARE")
        ]
        return earning_model

    @staticmethod
    def get_br_record_date_earnings(
            account: str,
            limit: int,
            earnings_types: List[EarningsTypes] = None,
    ) -> list:
        # query to find record date == 31-12-9999 (to be paid with no date specified)

        earnings_types_where_clause = (
            EarningsBrRecord.build_earnings_types_where_clause(earnings_types)
        )

        query = f"""
            SELECT MA.DESC_HIST_MVTO, MA.COD_NEG, MA.QTDE_MVTO, MA.PREC_LQDO/MA.QTDE_MVTO AS AMOUNT_PER_SHARE, 
            MA.PREC_LQDO, MA.DATA_MVTO                
            FROM CORRWIN.TCFMOVI_ACAO MA
            LEFT JOIN CORRWIN.TCFTIPO_MVTO TM ON TM.cod_tipo_mvto= MA.tipo_mvto
            WHERE COD_CLI = ('{account}') 
            {earnings_types_where_clause}
            AND DATA_MVTO = TO_DATE('31-DEC-9999', 'DD-MM-YYYY')
            AND MA.COD_NEG IS NOT NULL
            AND MA.QTDE_MVTO IS NOT NULL
            AND MA.DATA_MVTO IS NOT NULL
            FETCH NEXT {limit} ROWS ONLY
        """

        record_date_earnings_transactions = (
            EarningsClientRepository.get_data(
                sql=query
            )
        )

        earning_model = [
            EarningsBrRecord.build_br_earning_model(earning_transaction=earning_transaction)
            for earning_transaction in record_date_earnings_transactions if earning_transaction.get("AMOUNT_PER_SHARE")
        ]
        return earning_model

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
