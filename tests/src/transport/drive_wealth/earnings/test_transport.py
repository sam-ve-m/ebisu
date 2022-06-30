# STANDARD IMPORTS
from unittest.mock import patch
import pytest

# PROJECT IMPORTS
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.date_formatters.region.timestamp.model import RegionTimeStamp
from src.domain.statement.us.request.model import TransactionRequest, QueryParams
from src.transport.drive_wealth.earnings.transport import DwEarningsTransport
from tests.src.services.earnings_from_client.stub_earnings import dw_earnings_example


class Iterable:
    def __iter__(self):
        return self


get_transactions_stub = [{"dividend": {"type": "CASH",
                    "amountPerShare": 0.1511,
                    "taxCode": "FULLY_TAXABLE"
                },"instrument": {"id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "SPHD",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },"tranWhen": "2019-06-03T15:12:00.345Z",},
                 {"dividend": {"type": "CASH",
               "amountPerShare": 0.1511,
               "taxCode": "FULLY_TAXABLE"
               }, "instrument": {"id": "9563a550-9f3b-47aa-b570-f18435f218d2",
               "symbol": "SPHD",
               "name": "PowerShares S&P 500 High Div Low Vol ETF"
               }, "tranWhen": "2019-06-03T15:12:00.345Z", }]


@pytest.mark.asyncio
@patch.object(DwEarningsTransport, "_DwEarningsTransport__get_transactions", return_value=dw_earnings_example)
@patch.object(DwEarningsTransport, "_DwEarningsTransport__build_earning_model", return_value="")
async def test_get_us_transaction_earnings_when_sending_right_params_then_return_the_expected(
        mock_get_transactions
):
    Iterable.__next__ = mock_get_transactions
    response = await DwEarningsTransport.get_us_transaction_earnings(
        transaction_request=TransactionRequest(
            account='89c69304-018a-40b7-be5b-2121c16e109e.1651525277006',
            query_params=QueryParams(limit=1,
                                     offset=RegionTimeStamp(
                                         1642699893000, region_date_format=RegionDateFormat.US_DATE_FORMAT),
                                     from_date=RegionTimeStamp(
                                         1646757399000, region_date_format=RegionDateFormat.US_DATE_FORMAT),
                                     to_date=RegionTimeStamp(
                                         1648485399000, region_date_format=RegionDateFormat.US_DATE_FORMAT)
                                     )
        )
    )

    assert response == ""
