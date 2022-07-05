from typing import List

# from src.domain.statement.base.model.balance.model import Balance
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime
from src.domain.statement.base.model.region_date_format.enum import RegionDateFormat
from src.domain.statement.base.model.transaction.model import Transaction
from src.infrastructures.env_config import config
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class StatementsRepository(OracleBaseRepository):

    service = config("ORACLE_BASE_SERVICE_BR")
    user = config("ORACLE_BASE_USER")
    password = config("ORACLE_BASE_PASSWORD")
    base_dns = config("ORACLE_BASE_DSN")
    port = config("ORACLE_BASE_PORT")

    base_query = "SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO FROM CORRWIN.TCCMOVTO {0} ORDER BY NR_LANCAMENTO OFFSET {1} rows fetch first {2} row only"
    balance_query = "SELECT VL_TOTAL FROM CORRWIN.TCCSALREF WHERE CD_CLIENTE = {0}"

    @staticmethod
    def __list_paginated_account_transactions(
        where_clause: str,
        offset: int,
        limit: int,
    ):
        complete_transaction_query = StatementsRepository.base_query.format(
            where_clause, offset * 10, limit
        )

        transactions = StatementsRepository.get_data(sql=complete_transaction_query)

        transactions_model = [
            Transaction(
                description=transaction.get("DS_LANCAMENTO"),
                value=transaction.get("VL_LANCAMENTO"),
                date=RegionDateFormat.BR_DATE_FORMAT,
            )
            for transaction in transactions
        ]

        return transactions_model

    @staticmethod
    def list_paginated_complete_account_transactions(
        offset: int, limit: int, bmf_account: str
    ) -> List[Transaction]:
        where_clause = f"WHERE CD_CLIENTE = {bmf_account}"

        transactions_model = StatementsRepository.__list_paginated_account_transactions(
            where_clause=where_clause, offset=offset, limit=limit
        )

        return transactions_model

    @staticmethod
    def list_paginated_future_account_transactions(
        offset: int, limit: int, bmf_account: str
    ) -> List[Transaction]:
        where_clause = (
            f"WHERE CD_CLIENTE = {bmf_account} AND DT_LANCAMENTO > sysdate + 1"
        )

        transactions_model = StatementsRepository.__list_paginated_account_transactions(
            where_clause=where_clause, offset=offset, limit=limit
        )

        return transactions_model

    @staticmethod
    def list_paginated_outflow_account_transactions(
        offset: int, limit: int, bmf_account: str
    ) -> List[Transaction]:
        where_clause = f"WHERE CD_CLIENTE = {bmf_account} AND VL_LANCAMENTO < 0"

        transactions_model = StatementsRepository.__list_paginated_account_transactions(
            where_clause=where_clause, offset=offset, limit=limit
        )

        return transactions_model

    @staticmethod
    def list_paginated_inflow_account_transactions(
        offset: int, limit: int, bmf_account: str
    ) -> List[Transaction]:
        where_clause = f"WHERE CD_CLIENTE = {bmf_account} AND VL_LANCAMENTO > 0 "

        transactions_model = StatementsRepository.__list_paginated_account_transactions(
            where_clause=where_clause, offset=offset, limit=limit
        )

        return transactions_model

    # @staticmethod
    # def get_account_balance(bmf_account: str) -> Balance:
    #     balance = StatementsRepository.get_data(
    #         sql=StatementsRepository.balance_query.format(bmf_account)
    #     )
    #
    #     balance = balance[0].get("VL_TOTAL") if bool(balance) else 0.0
    #
    #     balance_model = Balance(
    #         value=balance
    #     )
    #
    #     return balance_model
