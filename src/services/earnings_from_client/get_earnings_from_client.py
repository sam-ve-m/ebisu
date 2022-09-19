# STANDARD LIBS
from datetime import datetime
from typing import Tuple, Callable

# PROJECT IMPORTS
from src.domain.date_formatters.region.timestamp.model import RegionTimeStamp
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.earning.br.response.model import BrEarningsModelToResponse
from src.domain.enums.region import Region
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from src.repositories.user_portfolios.repository import UserPortfoliosRepository
from src.domain.earning.us.response.model import (
    EarningsRecordResponse,
    EarningsModelToResponse,
)
from src.transport.drive_wealth.earnings.transport import DwEarningsTransport
from src.domain.earning.us.request.model import TransactionRequest, QueryParams
from src.transport.sinacor.earnings.transport import SinacorEarningsTransport


class EarningsFromClient:
    sinacor_earnings_transport = SinacorEarningsTransport

    @classmethod
    async def get_earnings_client_br_account(
        cls, earnings_client: EarningsClientModel, jwt_data: dict
    ) -> EarningsRecordResponse:

        portfolios = jwt_data.get("user", {}).get("portfolios", {})
        earnings_region = earnings_client.region.value
        region_portfolios = portfolios.get(earnings_region.lower(), {})

        account = cls.__extract_account(region_portfolios, earnings_client.region.value)

        unique_id = cls.__extract_unique_id_from_jwt(jwt_data=jwt_data)

        from_date, to_date = await EarningsFromClient.__get_range_date_and_offset(
            unique_id=unique_id, region=earnings_client.region, region_date_format=RegionDateFormat.BR_DATE_ISO_FORMAT
        )

        paid_transactions = await cls.sinacor_earnings_transport.paid_earnings(
            account=account, earnings_client=earnings_client, from_date=from_date, to_date=to_date
        )

        total_paid_earnings = sum(
            [paid_transaction.total for paid_transaction in paid_transactions]
        )

        (
            payable_transactions,
            record_transactions,
        ) = await cls.sinacor_earnings_transport.payable_and_record_date_earnings(
            account=account, earnings_client=earnings_client
        )

        earnings_br_transactions_response = BrEarningsModelToResponse.earnings_response(
            payable_transactions,
            paid_transactions,
            record_transactions,
            total_paid_earnings,
        )

        return earnings_br_transactions_response

    @classmethod
    async def get_earnings_client_us_account(
        cls, jwt_data: dict, earnings_client: EarningsClientModel
    ) -> EarningsRecordResponse:

        unique_id, account = EarningsFromClient.__extract_identifier_data_from_jwt(
            jwt_data=jwt_data
        )

        from_date, to_date = await EarningsFromClient.__get_range_date_and_offset(
            unique_id=unique_id, region=earnings_client.region, region_date_format=RegionDateFormat.US_DATE_FORMAT
        )

        transaction_request = TransactionRequest(
            account=account,
            query_params=QueryParams(
                from_date=from_date, to_date=to_date, limit=earnings_client.limit
            ),
        )

        earnings_us_transactions = (
            await DwEarningsTransport.get_us_transaction_earnings(
                transaction_request=transaction_request
            )
        )

        earnings_us_transactions_response = EarningsModelToResponse.earnings_response(
            earnings_us_transactions
        )

        return earnings_us_transactions_response

    @classmethod
    async def get_service_response(
        cls, earnings_client: EarningsClientModel, jwt_data: dict
    ) -> EarningsRecordResponse:

        map_key = earnings_client.region

        earnings_response = {
            Region.BR: EarningsFromClient.get_earnings_client_br_account,
            Region.US: EarningsFromClient.get_earnings_client_us_account,
        }
        resolver: Callable = earnings_response.get(map_key)
        resolver_response = list()
        if resolver:
            resolver_response = await resolver(
                jwt_data=jwt_data, earnings_client=earnings_client
            )

        return resolver_response

    @staticmethod
    async def __get_range_date_and_offset(
        unique_id: str, region: Region, region_date_format: RegionDateFormat
    ) -> Tuple[RegionTimeStamp, RegionTimeStamp]:

        from_raw_date = (
            await UserPortfoliosRepository.get_default_portfolio_created_at_by_region(
                unique_id=unique_id, region=region
            )
        )

        to_raw_date = int(datetime.now().timestamp() * 1000)

        from_date = RegionTimeStamp(
            timestamp=from_raw_date, region_date_format=region_date_format
        )
        to_date = RegionTimeStamp(
            timestamp=to_raw_date, region_date_format=region_date_format
        )

        return from_date, to_date


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
    def __extract_unique_id_from_jwt(jwt_data: dict) -> str:
        user = jwt_data.get("user", {})
        unique_id = user.get("unique_id")

        return unique_id

    @staticmethod
    def __extract_identifier_data_from_jwt(jwt_data: dict):
        user = jwt_data.get("user", {})
        account = user.get("portfolios", {}).get("us", {}).get("dw_account")

        unique_id = EarningsFromClient.__extract_unique_id_from_jwt(jwt_data=jwt_data)

        return unique_id, account
