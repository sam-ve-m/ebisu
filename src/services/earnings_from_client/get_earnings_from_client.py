# STANDARD LIBS
from datetime import datetime
from typing import Tuple

# PROJECT IMPORTS
from src.domain.date_formatters.region.timestamp.model import RegionTimeStamp
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.enums.region import Region
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from src.repositories.earnings.repository import EarningsClientRepository
from src.repositories.user_portfolios.repository import UserPortfoliosRepository
from src.services.earnings_from_client.strategies.br import GetBrEarningsDetails
from src.services.earnings_from_client.strategies.us import GetUsEarningsDetails


class EarningsFromClient:
    oracle_earnings_client_singleton_instance = EarningsClientRepository

    @staticmethod
    def __extract_account(portfolios: dict, region: str) -> str:
        accounts_by_region = {
            Region.BR.value: "bmf_account",
            Region.US.value: "dw_account",
        }
        fields = accounts_by_region[region]

        accounts = portfolios.get(fields)
        return accounts

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

    @classmethod
    def paid_earnings_data_response(
            cls, earnings_client: EarningsClientModel, accounts: str):

        paid_earnings_response = GetBrEarningsDetails.build_query_paid_earnings(
            cod_client=accounts,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
            earnings_types=earnings_client.earnings_types,
        )

        earnings_paid_values = [
            GetBrEarningsDetails.normalize_earnings_data(earnings_res)
            for earnings_res in paid_earnings_response
        ]
        return earnings_paid_values

    @classmethod
    def payable_earnings_data_response(
        cls, earnings_client: EarningsClientModel, accounts: str
    ):

        payable_earnings_response = GetBrEarningsDetails.build_query_payable_earnings(
            cod_client=accounts,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
            earnings_types=earnings_client.earnings_types,
        )

        earnings_payable_values = [
            GetBrEarningsDetails.normalize_earnings_data(earnings_res)
            for earnings_res in payable_earnings_response
        ]
        return earnings_payable_values

    @classmethod
    def record_date_earnings_response(
        cls, earnings_client: EarningsClientModel, accounts: str
    ):

        record_date_earnings_response = GetBrEarningsDetails.build_query_record_date_earnings(
            cod_client=accounts,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
            earnings_types=earnings_client.earnings_types,
        )

        record_date_earnings_values = [
            GetBrEarningsDetails.normalize_earnings_data(earnings_response)
            for earnings_response in record_date_earnings_response
        ]
        return record_date_earnings_values

    @classmethod
    async def get_earnings_client_br_account(cls, earnings_client: EarningsClientModel, jwt_data: dict):

        portfolios = jwt_data.get("user", {}).get("portfolios", {})

        region = earnings_client.region.value
        region_portfolios = portfolios.get(region.lower(), {})

        accounts = cls.__extract_account(region_portfolios, region)

        earnings_paid_values = EarningsFromClient.paid_earnings_data_response(
                earnings_client=earnings_client,
                accounts=accounts
            )

        earnings_payable_values = EarningsFromClient.payable_earnings_data_response(
                earnings_client=earnings_client,
                accounts=accounts,
            )

        earnings_record_date_values = EarningsFromClient.record_date_earnings_response(
                earnings_client=earnings_client,
                accounts=accounts,
            )

        response = {
            "paid_earnings": earnings_paid_values,
            "payable_earnings": earnings_payable_values,
            "record_date_earnings": earnings_record_date_values,
        }

        return response

    @classmethod
    async def get_earnings_client_us_account(cls, jwt_data: dict, earnings_client: EarningsClientModel):
        # us_portfolios = jwt_data.get("user", {}).get("portfolios", {}).get("us", {})
        # dw_account = us_portfolios.get("dw_account")
        dw_account = "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006"

        unique_id, account = EarningsFromClient.__extract_identifier_data_from_jwt(
            jwt_data=jwt_data
        )

        from_date, to_date, offset = await EarningsFromClient.__get_range_date_and_offset(
            unique_id=unique_id,
            requested_offset=earnings_client.offset
        )

        us_dividend = await GetUsEarningsDetails.get_dw_us_earnings(
            dw_account=dw_account,
            offset=offset,
            limit=earnings_client.limit,
            start_date=from_date,
            end_date=to_date,
        )

        if not us_dividend:
            return {}

        return us_dividend

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
