# Ebisu
from src.domain.exceptions.domain.model.forex.model import DataNotFoundInToken


class SimulationTokenModel:
    def __init__(self, token_decoded: dict):
        self.token_decoded = token_decoded
        self.forex_account = self.__get_forex_account()
        self.exchange_hash = self.__get_exchange_combination_hash()
        self.nature_operation = self.__get_nature_operation()
        self.net_value = self.__get_net_value()
        self.quantity_currency_traded = self.__get_quantity_currency_traded()

    def __get_forex_account(self):
        forex_account = self.token_decoded.get("CodigoCliente")
        if not forex_account:
            raise DataNotFoundInToken()
        return forex_account

    def __get_net_value(self):
        net_value = self.token_decoded.get("ValorLiquido")
        if not net_value:
            raise DataNotFoundInToken()
        return float(net_value)

    def __get_quantity_currency_traded(self):
        quantity_currency_traded = self.token_decoded.get("QuantidadeMoedaNegociada")
        if not quantity_currency_traded:
            raise DataNotFoundInToken()
        return float(quantity_currency_traded)

    def __get_nature_operation(self):
        nature_operation = self.token_decoded.get("CodigoNaturezaOperacao")
        if not nature_operation:
            raise DataNotFoundInToken()
        return int(nature_operation)

    def __get_exchange_combination_hash(self):
        base = self.token_decoded.get("SimboloMoedaBase")
        quote = self.token_decoded.get("SimboloMoedaCotacao")
        if not all([base, quote]):
            raise DataNotFoundInToken()
        exchange_combination_hash = f"{base}_TO_{quote}"
        return exchange_combination_hash
