from datetime import datetime, timedelta
from typing import Tuple

from src.domain.date_formatters.region.timestamp.model import RegionTimeStamp
from src.domain.enums.statement_type import StatementType
from src.domain.statement.base.model.region_date_format.enum import RegionDateFormat
from src.domain.statement.br.response.model import (
    StatementModelToResponse as BrStatementModelToResponse,
    StatementResponse as BrStatementResponse
)

from src.domain.statement.us.request.model import TransactionRequest, QueryParams
from src.domain.statement.us.response.model import (
    StatementModelToResponse as UsStatementModelToResponse,
    StatementResponse as UsStatementResponse
)

from src.domain.validators.exchange_info.get_statement_validator import (
    GetBrStatement, GetUsStatement,
)
from src.repositories.statements.repository import StatementsRepository
from src.repositories.user_portfolios.repository import UserPortfoliosRepository
from src.transport.drive_wealth.statement.transport import DwStatementTransport


class GetStatement:

    @classmethod
    async def get_br_bank_statement(cls, jwt_data: dict, statement: GetBrStatement) -> BrStatementResponse:

        list_statement_repository = {
            StatementType.ALL: StatementsRepository.list_paginated_complete_account_transactions,
            StatementType.FUTURE: StatementsRepository.list_paginated_future_account_transactions,
            StatementType.OUTFLOWS: StatementsRepository.list_paginated_outflow_account_transactions,
            StatementType.INFLOWS: StatementsRepository.list_paginated_inflow_account_transactions,
        }.get(statement.statement_type)

        bmf_account = GetStatement.__extract_bmf_account(jwt_data=jwt_data)

        transactions = list_statement_repository(
            offset=statement.offset,
            limit=statement.limit,
            bmf_account=bmf_account
        )

        statement_response = BrStatementModelToResponse.statement_response(
            transactions=transactions
        )

        return statement_response

    @staticmethod
    def __extract_bmf_account(jwt_data: dict) -> str:
        br_portfolios = jwt_data.get("user", {}).get("portfolios", {}).get("br", {})
        bmf_account = br_portfolios.get("bmf_account")

        return bmf_account

    @staticmethod
    async def get_us_bank_statement(jwt_data: dict, statement: GetUsStatement) -> UsStatementResponse:
        unique_id, account = GetStatement.__extract_identifier_data_from_jwt(
            jwt_data=jwt_data
        )

        get_rage_date_and_offset, get_transactions = {
            StatementType.ALL: (
                GetStatement.__get_range_date_and_offset,
                DwStatementTransport.get_transactions
            ),
            StatementType.FUTURE: (
                GetStatement.__get_future_range_date_and_offset,
                DwStatementTransport.get_transactions
            ),
            StatementType.OUTFLOWS: (
                GetStatement.__get_range_date_and_offset,
                DwStatementTransport.get_outflow_transactions
            ),
            StatementType.INFLOWS: (
                GetStatement.__get_range_date_and_offset,
                DwStatementTransport.get_inflow_transactions
            ),
        }.get(statement.statement_type)

        from_date, to_date, offset = await get_rage_date_and_offset(
            unique_id=unique_id,
            requested_offset=statement.offset
        )

        transaction_request = TransactionRequest(
            account=account,
            query_params=QueryParams(
                from_date=from_date,
                to_date=to_date,
                offset=offset,
                limit=statement.limit,
            )
        )

        transactions = await get_transactions(
            transaction_request=transaction_request
        )

        statement_response = UsStatementModelToResponse.statement_response(
            transactions=transactions
        )

        return statement_response

    @staticmethod
    def __extract_identifier_data_from_jwt(jwt_data: dict):
        user = jwt_data.get("user", {})
        account = user.get("portfolios", {}).get("us", {}).get("dw_account")

        unique_id = user.get("unique_id")

        return unique_id, account

    @staticmethod
    async def __get_range_date_and_offset(
        unique_id: str,
        requested_offset: int
    ) -> Tuple[RegionTimeStamp, RegionTimeStamp, RegionTimeStamp]:

        from_raw_date = await UserPortfoliosRepository.get_default_portfolio_created_at_by_region(
            unique_id=unique_id,
            region="US"
        )

        to_raw_date = datetime.now().timestamp() * 1000

        requested_raw_offset = GetStatement.__get_offset(
            requested_offset=requested_offset,
            from_date=from_raw_date
        )

        from_date = RegionTimeStamp(timestamp=from_raw_date, region_date_format=RegionDateFormat.US_DATE_FORMAT)
        to_date = RegionTimeStamp(timestamp=to_raw_date, region_date_format=RegionDateFormat.US_DATE_FORMAT)
        requested_offset = RegionTimeStamp(
            timestamp=requested_raw_offset,
            region_date_format=RegionDateFormat.US_DATE_FORMAT
        )

        return from_date, to_date, requested_offset

    @staticmethod
    async def __get_future_range_date_and_offset(
        unique_id: str,
        requested_offset: int
    ) -> Tuple[RegionTimeStamp, RegionTimeStamp, RegionTimeStamp]:

        from_raw_date = datetime.now().timestamp() * 1000
        to_raw_date = (datetime.now() + timedelta(days=30)).timestamp() * 1000

        requested_raw_offset = GetStatement.__get_offset(
            requested_offset=requested_offset,
            from_date=from_raw_date
        )

        from_date = RegionTimeStamp(timestamp=from_raw_date, region_date_format=RegionDateFormat.US_DATE_FORMAT)
        to_date = RegionTimeStamp(timestamp=to_raw_date, region_date_format=RegionDateFormat.US_DATE_FORMAT)
        requested_offset = RegionTimeStamp(
            timestamp=requested_raw_offset,
            region_date_format=RegionDateFormat.US_DATE_FORMAT
        )

        return from_date, to_date, requested_offset

    @staticmethod
    def __get_offset(requested_offset: int, from_date: int):
        if requested_offset is None:
            requested_offset = from_date

        return requested_offset

