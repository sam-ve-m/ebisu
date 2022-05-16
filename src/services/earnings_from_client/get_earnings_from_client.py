# EXTERNAL LIBS
from src.domain.enums.region import Region
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from src.repositories.earnings.repository import EarningsClientRepository
from src.services.earnings_from_client.strategies import earnings_client_region


class EarningsFromClient:
    oracle_earnings_client_singleton_instance = EarningsClientRepository

    @staticmethod
    def get_account_by_region(portfolios: dict, region: str) -> str:

        accounts_by_region = {
            Region.BR.value: ["bovespa_account", "bmf_account"],
            Region.US.value: ["dw_id", "dw_account"],
        }

        field = accounts_by_region[region]
        return portfolios.get(field)

    @classmethod
    def normalize_earnings_data(cls, client_earnings: dict) -> dict:

        normalized_data = {
            "client_code": client_earnings.get("COD_CLI"),
            "trade_history": client_earnings.get("DESC_HIST_MVTO"),
            "trade_type": client_earnings.get("DESC_RESU_TIPO_MOVTO"),
            "trade_code": client_earnings.get("COD_NEG"),
            "transaction_amount": client_earnings.get("QTDE_MVTO"),
            "net_price": client_earnings.get("PREC_LQDO"),
            "transaction_date": client_earnings.get("DATA_MVTO"),
        }

        return normalized_data

    @classmethod
    def get_service_response(
        cls, earnings_client: EarningsClientModel, jwt_data: dict
    ) -> dict:

        region = earnings_client.region.value
        open_earnings = earnings_client_region[region]

        # query result of EXPECTED earnings values (with the date informed)
        query_payable_values = open_earnings.build_query_payable_earnings(
            cod_client=earnings_client.cod_client,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
        )

        payable_earnings_request = open_earnings.oracle_earnings_client_singleton_instance.get_data(
            sql=query_payable_values
        )

        earnings_payable_values = [
            EarningsFromClient.normalize_earnings_data(earnings_res)
            for earnings_res in payable_earnings_request
        ]

        # query result of EXPECTED earnings values (31-12-9999)
        query_record_date_values = open_earnings.build_query_record_date_earnings(
            cod_client=earnings_client.cod_client,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
        )

        record_date_earnings_request = open_earnings.oracle_earnings_client_singleton_instance.get_data(
            sql=query_record_date_values
        )

        earnings_record_date_values = [
            EarningsFromClient.normalize_earnings_data(earnings_response)
            for earnings_response in record_date_earnings_request
        ]

        response = {
            "payable_earnings": earnings_payable_values,
            "record_date_earnings": earnings_record_date_values,
        }

        return response
