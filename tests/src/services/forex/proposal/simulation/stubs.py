# Ebisu
from src.domain.request.forex.currency_options import CurrencyExchange
from src.domain.models.forex.proposal.simulation_request_data.model import (
    SimulationModel,
)

# Third party
from caronte import CaronteStatus


stub_currency_exchange = CurrencyExchange(
    **{"base": "BRL", "quote": "USD", "quantity": 105}
)

stub_response_rote_21 = {
    "cliente": {"codigo": 208785},
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
            "tipoParidade": None,
        },
        "moedaCotacao": {
            "codigoBACEN": 220,
            "simbolo": "USD",
            "precisao": 0,
            "prioritaria": False,
            "tipoParidade": None,
        },
        "data": "2022-09-12T16:23:00Z",
        "validade": "2022-09-12T16:27:14Z",
    },
}
stub_base_url = "https://sbxapi.ourinvest.com.br:43400/api/v1"
stub_current_quote_url = (
    "produto/cambio/naturezaOperacao/{}/taxa/{}/{}/cliente/{}/spread/{}"
)
stub_customer_exchange_data = {
    "account_number": 12345,
    "base_currency": "BRL",
    "quote_currency": "USD",
    "spread": 0.02,
}

stub_simulation_model = SimulationModel(
    client_id=12345,
    payload=stub_currency_exchange,
    customer_exchange_data=stub_customer_exchange_data,
)

stub_config_path_quotation = [
    "https://sbxapi.ourinvest.com.br:43400/api/v1",
    "produto/cambio/naturezaOperacao/{}/taxa/{}/{}/cliente/{}/spread/{}",
    "https://sbxapi.ourinvest.com.br:43400/api/v1",
    "produto/cambio/naturezaOperacao/{}/taxa/{}/{}/cliente/{}/spread/{}",
]

stub_config_path_exchange_simulation = [
    "https://sbxapi.ourinvest.com.br:43400/api/v1",
    "operacao/cambio/calcular",
]

stub_token_generated_in_route_21 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJDb2RpZ29DbGllbnRlIjoiMjA4Nzg1IiwiVGF4YUNvbWVyY2lhbCI6IjUuMjMzMCIsIlBlcmNlbnR1YWxTcHJlYWQiOiIwLjAyMDAiLCJWYWxvckNvdGFjYW9DYW1iaW8iOiI1LjMzNzciLCJNb2VkYUJhc2VDb2RpZ29CQUNFTiI6Ijc5MCIsIk1vZWRhQmFzZVNpbWJvbG8iOiJCUkwiLCJNb2VkYUNvdGFjYW9Db2RpZ29CQUNFTiI6IjIyMCIsIk1vZWRhQ290YWNhb1NpbWJvbG8iOiJVU0QiLCJEYXRhQ290YWNhbyI6IjE2NjI5OTk3ODAiLCJEYXRhVmFsaWRhZGUiOiIxNjYzMDAwMDM0IiwiRGF0YVBhZ2FtZW50byI6IjE2NjI5NTE2MDAiLCJ0cCI6IlVHVGplMjRGZ3dGRzV5Q2pXL3FLeFE9PSIsIkNvZGlnb05hdHVyZXphT3BlcmFjYW8iOiI0IiwibmJmIjoxNjYyOTk5NzgwLCJleHAiOjE2NjMwMDAwMzQsImlhdCI6MTY2Mjk5OTk3NCwiaXNzIjoiMjA4Nzg1In0.wleiicCFoChvF9Jgj5WHlbO6Hhnpy0RNXl2HEAXyVIs"

stub_response_rote_22 = {
    "valores": {
        "codigoCliente": 208785,
        "codigoNaturezaOperacao": 4,
        "simboloMoedaBase": "BRL",
        "simboloMoedaCotacao": "USD",
        "quantidadeMoedaNegociada": 18.53,
        "valorCotacaoCambio": 5.33759378,
        "valorTarifa": 0.0,
        "valorBruto": 98.91,
        "percentualIOF": 1.100000,
        "valorIOF": 1.09,
        "valorLiquido": 100.00,
        "vet": 5.3967,
        "dataCotacao": "2022-09-14T19:18:52Z",
        "dataValidade": "2022-09-14T19:28:03Z",
        "dataPagamento": "2022-09-14T03:00:00Z",
        "percentualSpread": 0.0200,
        "taxaComercial": 5.2330,
    },
    "controle": {
        "codigo": "ope.cmb.coc.001",
        "mensagem": "Valores calculados com sucesso.",
        "token": None,
        "dataHoraServidor": "2022-09-14T19:26:06Z",
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJDb2RpZ29DbGllbnRlIjoiMjA4Nzg1IiwiQ29kaWdvTmF0dXJlemFPcGVyYWNhbyI6IjQiLCJTaW1ib2xvTW9lZGFCYXNlIjoiQlJMIiwiU2ltYm9sb01vZWRhQ290YWNhbyI6IlVTRCIsIlF1YW50aWRhZGVNb2VkYU5lZ29jaWFkYSI6IjE4LjUzIiwiVmFsb3JDb3RhY2FvQ2FtYmlvIjoiNS4zMzc1OTM3OCIsIlZhbG9yVGFyaWZhIjoiMCIsIlZhbG9yQnJ1dG8iOiI5OC45MSIsIlBlcmNlbnR1YWxJT0YiOiIxLjEwMDAwMCIsIlZhbG9ySU9GIjoiMS4wOSIsIlZhbG9yTGlxdWlkbyI6IjEwMC4wMCIsIkRhdGFDb3RhY2FvIjoiMTY2MzE4MzEzMiIsIkRhdGFWYWxpZGFkZSI6IjE2NjMxODM2ODMiLCJEYXRhUGFnYW1lbnRvIjoiMTY2MzEzNTIwMCIsIlBlcmNlbnR1YWxTcHJlYWQiOiIwLjAyMDAiLCJUYXhhQ29tZXJjaWFsIjoiNS4yMzMwIiwidHAiOiJSdjNtZmlUTDhzQm9xaGFPb0FKY2lRPT0iLCJuYmYiOjE2NjMxODMxMzIsImV4cCI6MTY2MzE4MzY4MywiaWF0IjoxNjYzMTgzNTY2LCJpc3MiOiIyMDg3ODUifQ.B4K40zUrKxvk5FRBfQubG2kjIHry018fwWSMZx-Jx_w",
}

stub_response_missing_data_rote_22 = {
    "valores": {
        "codigoCliente": 208785,
        "codigoNaturezaOperacao": 4,
        "simboloMoedaBase": "BRL",
        "simboloMoedaCotacao": "USD",
        "quantidadeMoedaNegociada": 18.53,
        "valorCotacaoCambio": 5.33759378,
        "valorTarifa": 0.0,
        "valorBruto": 98.91,
        "percentualIOF": 1.100000,
        "valorIOF": 1.09,
        "valorLiquido": 100.00,
        "vet": 5.3967,
        "dataCotacao": "2022-09-14T19:18:52Z",
        "dataValidade": "2022-09-14T19:28:03Z",
        "dataPagamento": "2022-09-14T03:00:00Z",
        "percentualSpread": 0.0200,
        "taxaComercial": 5.2330,
    },
    "controle": {
        "codigo": "ope.cmb.coc.001",
        "mensagem": "Valores calculados com sucesso.",
        "token": None,
        "dataHoraServidor": "2022-09-14T19:26:06Z",
    },
}

stub_caronte_response_success_21 = (True, CaronteStatus.SUCCESS, stub_response_rote_21)
stub_caronte_response_success_22 = (True, CaronteStatus.SUCCESS, stub_response_rote_22)
stub_caronte_response_bad_request = (False, CaronteStatus.BAD_REQUEST, None)
stub_caronte_response_unauthorized = (False, CaronteStatus.UNAUTHORIZED, None)
stub_caronte_response_forbidden = (False, CaronteStatus.FORBIDDEN, None)
stub_caronte_response_token_not_found = (False, CaronteStatus.TOKEN_NOT_FOUND, None)
stub_caronte_response_unexpected_error = (False, CaronteStatus.UNEXPECTED_ERROR, None)
