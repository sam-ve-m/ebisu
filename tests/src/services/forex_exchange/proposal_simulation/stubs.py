from src.domain.validators.forex_exchange.currency_options import CurrencyExchange
from src.domain.models.forex_exchange.customer_exchange_request_data.model import CustomerExchangeRequestModel
from caronte import CaronteStatus


stub_currency_exchange = CurrencyExchange(**{
    "base": "BRL",
    "quote": "USD",
    "quantity": 105
})

stub_customer_token = {
    "cliente": {
        "codigo": 208785
    },
    "dataPagamento": "2022-09-12T03:00:00Z",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJDb2RpZ29DbGllbnRlIjoiMjA4Nzg1IiwiVGF4YUNvbWVyY2lhbCI6IjUuMjMzMCIsIlBlcmNlbnR1YWxTcHJlYWQiOiIwLjAyMDAiLCJWYWxvckNvdGFjYW9DYW1iaW8iOiI1LjMzNzciLCJNb2VkYUJhc2VDb2RpZ29CQUNFTiI6Ijc5MCIsIk1vZWRhQmFzZVNpbWJvbG8iOiJCUkwiLCJNb2VkYUNvdGFjYW9Db2RpZ29CQUNFTiI6IjIyMCIsIk1vZWRhQ290YWNhb1NpbWJvbG8iOiJVU0QiLCJEYXRhQ290YWNhbyI6IjE2NjI5OTk3ODAiLCJEYXRhVmFsaWRhZGUiOiIxNjYzMDAwMDM0IiwiRGF0YVBhZ2FtZW50byI6IjE2NjI5NTE2MDAiLCJ0cCI6IlVHVGplMjRGZ3dGRzV5Q2pXL3FLeFE9PSIsIkNvZGlnb05hdHVyZXphT3BlcmFjYW8iOiI0IiwibmJmIjoxNjYyOTk5NzgwLCJleHAiOjE2NjMwMDAwMzQsImlhdCI6MTY2Mjk5OTk3NCwiaXNzIjoiMjA4Nzg1In0.wleiicCFoChvF9Jgj5WHlbO6Hhnpy0RNXl2HEAXyVIs",
    "taxa": {
        "taxaComercial": 5.2330,
        "percentualSpread": 0.0200,
        "valorTotal": 5.3377,
        "moedaBase": {
            "codigoBACEN": 790,
            "simbolo": "BRL",
            "precisao": 0,
            "prioritaria": False,
            "tipoParidade": None
        },
        "moedaCotacao": {
            "codigoBACEN": 220,
            "simbolo": "USD",
            "precisao": 0,
            "prioritaria": False,
            "tipoParidade": None
        },
        "data": "2022-09-12T16:23:00Z",
        "validade": "2022-09-12T16:27:14Z"
    }
}
stub_base_url = "https://sbxapi.ourinvest.com.br:43400/api/v1"
stub_current_quote_url = "produto/cambio/naturezaOperacao/{}/taxa/{}/{}/cliente/{}/spread/{}"
stub_customer_exchange_data = {
    "exchange_account_id": 12345,
    "base_currency": "BRL",
    "quote_currency": "USD",
    "spread": 0.02
}

stub_customer_exchange_request_model = CustomerExchangeRequestModel(
    exchange_account_id=12345,
    currency_exchange=stub_currency_exchange,
    customer_exchange_data=stub_customer_exchange_data
)

stub_caronte_response_success = (True, CaronteStatus.SUCCESS, stub_customer_token)
stub_caronte_response_bad_request = (False, CaronteStatus.BAD_REQUEST, None)
stub_caronte_response_unauthorized = (False, CaronteStatus.UNAUTHORIZED, None)
stub_caronte_response_forbidden = (False, CaronteStatus.FORBIDDEN, None)
stub_caronte_response_token_not_found = (False, CaronteStatus.TOKEN_NOT_FOUND, None)
stub_caronte_response_unexpected_error = (False, CaronteStatus.UNEXPECTED_ERROR, None)

stub_config_path = ["https://sbxapi.ourinvest.com.br:43400/api/v1", "produto/cambio/naturezaOperacao/{}/taxa/{}/{}/cliente/{}/spread/{}", "https://sbxapi.ourinvest.com.br:43400/api/v1", "produto/cambio/naturezaOperacao/{}/taxa/{}/{}/cliente/{}/spread/{}"]
