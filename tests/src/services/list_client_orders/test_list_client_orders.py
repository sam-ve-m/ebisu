# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# Internal Libs
from src.domain.enums.region import Region
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository
from src.services.list_client_orders.list_client_orders import ListOrders
from src.services.list_client_orders.strategies import GetBrOrders
from tests.src.stubs.project_stubs.stub_data import (
    StubCompanyInformationRepository,
    payload_data_dummy,
    payload_invalid_data_dummy,
)
from tests.src.stubs.project_stubs.stub_list_client_orders import (
    user_trade_dummy,
    normalized_data_dummy,
    data_response_stub,
    get_data_stub,
    normalized_data_stub,
    get_data_two_status_stub,
    normalized_data_second_status,
    data_two_response,
)

list_data_dummy = ["NEW", "FILLED"]


def test_when_sending_two_order_status_then_return_the_splited_data_as_expected():
    data_to_split = "NEW|FILLED"
    pipe_to_list_response = ListOrders.pipe_to_list(data=data_to_split)
    assert pipe_to_list_response == list_data_dummy
    assert isinstance(pipe_to_list_response, list)


def test_when_sending_user_trade_and_field_to_decimal_converter_then_return_the_expected():
    response = ListOrders.decimal_128_converter(
        user_trade=user_trade_dummy, field="AVGPX"
    )
    assert response == 0.0
    assert type(response) is int


@pytest.mark.asyncio
async def test_when_sending_the_right_params_to_get_company_name_then_return_the_expected():
    symbol_dummy = None
    ListOrders.company_information_repository = StubCompanyInformationRepository
    response = await ListOrders.company_information_repository.get_company_name(
        symbol=symbol_dummy
    )
    assert response is None


@pytest.mark.asyncio
@patch(
    "src.services.list_client_orders.list_client_orders.CompanyInformationRepository.get_company_name",
    return_value="Iochpe Maxion SA",
)
async def test_when_sending_the_user_trade_params_then_return_the_normalized_data(
    mock_normalize_open_order,
):
    response = await ListOrders.normalize_open_order(
        user_trade=user_trade_dummy, region=Region.BR
    )
    assert response == normalized_data_dummy
    mock_normalize_open_order.assert_called_with("MYPK3")
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch(
    "src.repositories.companies_data.repository.CompanyInformationRepository.get_company_name"
)
async def test_when_sending_the_right_params_to_get_company_name_then_return_the_expected(
    mock_get_company_name,
):
    symbol_dummy = "MYPK3"
    ListOrders.company_information_repository = StubCompanyInformationRepository
    response = await ListOrders.company_information_repository.get_company_name(
        symbol=symbol_dummy
    )
    assert response == "Iochpe Maxion SA"
    assert isinstance(response, str)


@pytest.mark.asyncio
@patch.object(GetBrOrders, "build_query", return_value=MagicMock())
@patch.object(OracleBaseRepository, "get_data", return_value=get_data_two_status_stub)
@patch.object(ListOrders, "get_accounts_by_region", return_value=["000000014-6", "14"])
@patch.object(ListOrders, "decimal_128_converter", return_value=0)
@patch.object(
    ListOrders,
    "normalize_open_order",
    side_effect=[normalized_data_stub, normalized_data_second_status],
)
@patch.object(ListOrders, "pipe_to_list", return_value=["NEW", "CANCELLED"])
@patch("src.services.list_client_orders.list_client_orders.order_region")
async def test_when_sending_the_right_params_and_single_order_status_then_return_the_expected(
    mock_order_region,
    mock_pipe_to_list,
    normalize_open_order,
    decimal_128_converter,
    get_accounts_by_region,
    mock_get_data,
    mock_build_query,
):
    mock_order_region.__getitem__ = MagicMock(return_value=GetBrOrders)
    response = await ListOrders.get_service_response(
        jwt_data=payload_data_dummy,
        list_client_orders=MagicMock(
            region=MagicMock(value="BR"), order_status=["NEW", "CANCELLED"]
        ),
    )
    assert response == list(data_two_response)
    assert response[0]["status"] == "NEW"
    assert response[0]["symbol"] == "JBSS3"
    assert response[1]["status"] == "CANCELLED"
    assert response[1]["symbol"] == "VALE3"
    assert isinstance(response, list)


# this test has passed
@pytest.mark.asyncio
@patch.object(GetBrOrders, "build_query", return_value=MagicMock())
@patch.object(OracleBaseRepository, "get_data", return_value=get_data_stub)
@patch.object(ListOrders, "get_accounts_by_region", return_value=["000000014-6", "14"])
@patch.object(ListOrders, "decimal_128_converter", return_value=0)
@patch.object(ListOrders, "normalize_open_order", return_value=normalized_data_stub)
@patch("src.services.list_client_orders.list_client_orders.order_region")
async def test_when_sending_the_right_params_and_two_order_status_then_return_the_expected(
    mock_order_region,
    normalize_open_order,
    decimal_128_converter,
    get_accounts_by_region,
    mock_get_data,
    mock_build_query,
):
    mock_order_region.__getitem__ = MagicMock(return_value=GetBrOrders)
    response = await ListOrders.get_service_response(
        jwt_data=payload_data_dummy,
        list_client_orders=MagicMock(
            region=MagicMock(value="BR"), order_status=["FILLED"]
        ),
    )
    assert response == list(data_response_stub)
    assert response[0]["name"] == "JBS SA"
    assert response[0]["symbol"] == "JBSS3"
    assert isinstance(response, list)


@pytest.mark.asyncio
async def test_when_sending_wrong_params_then_return_an_empty_object():
    with pytest.raises(AttributeError) as err:
        response = await ListOrders.get_service_response(
            jwt_data=MagicMock(),
            list_client_orders=MagicMock(region=MagicMock(value=None), order_status=[]),
        )
        assert response == "'NoneType' object has no attribute 'lower'"


@pytest.mark.asyncio
async def test_when_jwt_data_payload_is_invalid_then_check_if_portfolios_is_in_the_payload_response():
    with pytest.raises(AttributeError) as err:
        response = await ListOrders.get_service_response(
            jwt_data=payload_invalid_data_dummy,
            list_client_orders=MagicMock(region="BR", order_status=MagicMock()),
        )
        assert response == AttributeError


@pytest.mark.asyncio
async def test_when_jwt_data_payload_is_none_then_raise_attribute_error():
    with pytest.raises(AttributeError) as err:
        response = await ListOrders.get_service_response(
            jwt_data="",
            list_client_orders=MagicMock(region="BR", order_status=MagicMock()),
        )
        assert response == AttributeError
