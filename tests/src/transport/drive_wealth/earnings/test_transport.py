# STANDARD IMPORTS
from unittest.mock import patch
from datetime import datetime
import pytest

# PROJECT IMPORTS
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.date_formatters.region.timestamp.model import RegionTimeStamp
from src.domain.statement.us.request.model import TransactionRequest, QueryParams
from src.transport.drive_wealth.earnings.transport import DwEarningsTransport
from tests.src.transport.drive_wealth.earnings.stub_transport import (
    get_transactions_model_stub,
    get_transactions_stub,
)


class Iterable:
    def __iter__(self):
        return self


@pytest.mark.asyncio
@patch.object(
    DwEarningsTransport,
    "_DwEarningsTransport__get_transactions",
    return_value=get_transactions_stub,
)
@patch.object(
    DwEarningsTransport,
    "_DwEarningsTransport__build_earning_model",
    side_effect=[get_transactions_model_stub, {}],
)
async def test_get_us_transaction_earnings_when_sending_right_params_then_return_the_expected(
    mock_get_transactions, mock_build_earning_model
):
    Iterable.__next__ = mock_get_transactions
    response = await DwEarningsTransport.get_us_transaction_earnings(
        transaction_request=TransactionRequest(
            account="89c69304-018a-40b7-be5b-2121c16e109e.1651525277006",
            query_params=QueryParams(
                limit=1,
                offset=RegionTimeStamp(
                    timestamp=1642699893000,
                    region_date_format=RegionDateFormat.US_DATE_FORMAT,
                ),
                from_date=RegionTimeStamp(
                    timestamp=1646757399000,
                    region_date_format=RegionDateFormat.US_DATE_FORMAT,
                ),
                to_date=RegionTimeStamp(
                    timestamp=1648485399000,
                    region_date_format=RegionDateFormat.US_DATE_FORMAT,
                ),
            ),
        )
    )

    assert response == [get_transactions_model_stub]
    assert isinstance(response, list)


@pytest.mark.asyncio
async def test_get_us_transaction_earnings_when_sending_wrong_params_then_return_the_expected():
    with pytest.raises(AttributeError):
        await DwEarningsTransport.get_us_transaction_earnings(
            transaction_request=TransactionRequest(
                account=None,
                query_params=QueryParams(
                    limit=1,
                    offset=None,
                    from_date=None,
                    to_date=RegionTimeStamp(
                        timestamp=1648485399000,
                        region_date_format=RegionDateFormat.US_DATE_FORMAT,
                    ),
                ),
            )
        )
