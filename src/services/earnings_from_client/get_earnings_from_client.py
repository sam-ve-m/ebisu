# STANDARD LIBS
from datetime import datetime
from typing import Tuple

# PROJECT IMPORTS
from src.domain.date_formatters.region.timestamp.model import RegionTimeStamp
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.earning.br.response.model import BrEarningsModelToResponse
from src.domain.enums.region import Region
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from src.repositories.earnings.repository import EarningsClientRepository, EarningsBrRecord
from src.repositories.user_portfolios.repository import UserPortfoliosRepository
from src.domain.earning.us.response.model import EarningsRecordResponse, EarningsModelToResponse
from src.transport.drive_wealth.earnings.transport import DwEarningsTransport
from src.domain.statement.us.request.model import TransactionRequest, QueryParams
# from src.domain.earning.br.request.model import QueryBrParams, TransactionBrRequest


class EarningsFromClient:
    oracle_earnings_client_singleton_instance = EarningsClientRepository

    @classmethod
    async def get_earnings_client_br_account(cls, earnings_client: EarningsClientModel, jwt_data: dict):

        portfolios = jwt_data.get("user", {}).get("portfolios", {})
        earnings_region = earnings_client.region.value
        region_portfolios = portfolios.get(earnings_region.lower(), {})

        account = cls.__extract_account(region_portfolios, earnings_client.region.value)

        payable_transactions = EarningsBrRecord.get_br_payable_earnings(
            account=account,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
            earnings_types=earnings_client.earnings_types
        )

        paid_transactions = EarningsBrRecord.get_br_paid_earnings(
            account=account,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
            earnings_types=earnings_client.earnings_types
        )

        record_transactions = EarningsBrRecord.get_br_record_date_earnings(
            account=account,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
            earnings_types=earnings_client.earnings_types
        )

        earnings_us_transactions_response = BrEarningsModelToResponse.earnings_response(
            payable_transactions, paid_transactions, record_transactions
        )

        return earnings_us_transactions_response

    @classmethod
    async def get_earnings_client_us_account(
            cls, jwt_data: dict, earnings_client: EarningsClientModel
    ) -> EarningsRecordResponse:

        unique_id, account = EarningsFromClient.__extract_identifier_data_from_jwt(
            jwt_data=jwt_data
        )

        from_date, to_date, offset = await EarningsFromClient.__get_range_date_and_offset(
            unique_id=unique_id,
            requested_offset=earnings_client.offset
        )

        transaction_request = TransactionRequest(
            account=account,
            query_params=QueryParams(
                from_date=from_date,
                to_date=to_date,
                offset=offset,
                limit=earnings_client.limit
            )
        )

        earnings_us_transactions = await DwEarningsTransport.get_us_transaction_earnings(
            transaction_request=transaction_request
        )

        earnings_us_transactions_response = EarningsModelToResponse.earnings_response(
                earnings_us_transactions
            )

        return earnings_us_transactions_response

    @classmethod
    async def get_service_response(
        cls, earnings_client: EarningsClientModel, jwt_data: dict
    ) -> dict:

        map_key = earnings_client.region

        earnings_response = {
            Region.BR: EarningsFromClient.get_earnings_client_br_account,
            Region.US: EarningsFromClient.get_earnings_client_us_account,
        }

        earnings_client = await earnings_response.get(map_key, [])(
            jwt_data=jwt_data,
            earnings_client=earnings_client
        )

        return earnings_client

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

        requested_raw_offset = EarningsFromClient.__get_offset(
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
    def __extract_account(portfolios: dict, region: str) -> str:
        accounts_by_region = {
            Region.BR.value: "bmf_account",
            Region.US.value: "dw_account",
        }
        fields = accounts_by_region[region]

        account = portfolios.get(fields)
        return account

    @staticmethod
    def __get_offset(requested_offset: int, from_date: int):
        if requested_offset is None:
            requested_offset = from_date

        return requested_offset

    @staticmethod
    def __extract_identifier_data_from_jwt(jwt_data: dict):
        user = jwt_data.get("user", {})
        account = user.get("portfolios", {}).get("us", {}).get("dw_account")

        unique_id = user.get("unique_id")

        return unique_id, account
