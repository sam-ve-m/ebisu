# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# Internal Libs
from src.domain.enums.region import Region
from src.services.orders.strategies.br_orders.strategy import (
    GetBrOrders,
)
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository
from src.services.orders.orders import Orders
from tests.src.stubs.project_stubs.stub_data import payload_data_dummy
from tests.src.stubs.project_stubs.stub_get_client_orders import (
    user_open_orders_dummy,
    query_dummy_get_client,
    dummy_user_trade,
    dummy_normalized_data,
    client_order_response_dummy,
    clorder_invalid_params_us,
)


def test_decimal_converter_when_sending_user_trade_and_field_to_decimal_converter_then_return_the_expected():
    response = Orders.decimal_128_converter(user_trade=dummy_user_trade, field="AVGPX")
    assert response == 0.0
    assert type(response) is int


def test_normalized_data_when_sending_the_user_trade_params_then_return_the_normalized_data():
    response = Orders.normalize_client_orders_open_order(
        user_trade=dummy_user_trade, region=Region.BR
    )
    assert response == dummy_normalized_data
    assert isinstance(response, dict)


def test_tiff_response_converter_when_sending_right_params_then_return_the_expected():
    response = Orders.tiff_response_converter(tif_value="DAY")
    assert response == "DAY"
    assert isinstance(response, str)


def test_tiff_response_converter_when_sending_no_params_then_return_the_expected():
    response = Orders.tiff_response_converter(tif_value="")
    assert response == "NA"
    assert isinstance(response, str)


@patch.object(GetBrOrders, "build_query", return_value=query_dummy_get_client)
@patch.object(OracleBaseRepository, "get_data", return_value=user_open_orders_dummy)
@patch("src.services.list_client_orders.list_client_orders.order_region")
def test_get_service_response_when_sending_the_right_paramks_then_return_the_expected(
    mock_order_region, mock_build_query, mock_get_data
):
    mock_order_region.__getitem__ = MagicMock(return_value=GetBrOrdersDetails)
    response = Orders.get_client_orders(
        client_order=MagicMock(
            region=Region.BR, cl_order_id="008cf873-ee2a-4b08-b277-74b8b17f6e64"
        ),
        jwt_data=payload_data_dummy,
    )

    assert response == client_order_response_dummy
    assert response[0]["symbol"] == "VALE3"
    assert isinstance(response, list)


@patch.object(GetBrOrders, "build_query", return_value="")
@patch.object(OracleBaseRepository, "get_data", return_value="")
@patch("src.services.list_client_orders.list_client_orders.order_region")
def test_get_service_response_when_sending_the_right_params_then_return_empty_object(
    mock_order_region, mock_build_query, mock_get_data
):
    mock_order_region.__getitem__ = MagicMock(return_value=GetBrOrders)
    response = Orders.get_client_orders(
        client_order=MagicMock(
            region=MagicMock(value="BR"),
            cl_order_id="008cf873-ee2a-4b08-b277-74b8b17f6e64",
        ),
        jwt_data=payload_data_dummy,
    )

    assert response == []
    assert isinstance(response, list)


def test_cl_order_get_service_response_when_the_params_are_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError) as err:
        Orders.get_client_orders(client_order=clorder_invalid_params_us, jwt_data="")
        assert err == "'str' object has no attribute 'get'"


def test_cl_order_get_service_response_when_the_statement_params_are_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError) as err:
        Orders.get_client_orders(client_order="", jwt_data=payload_data_dummy)
        assert err == "AttributeError: 'str' object has no attribute 'region'"
