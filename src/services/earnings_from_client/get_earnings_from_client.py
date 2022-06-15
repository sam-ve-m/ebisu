# INTERNAL LIBS
from src.domain.enums.region import Region
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from src.repositories.earnings.repository import EarningsClientRepository
from src.services.earnings_from_client.strategies import earnings_client_region


class EarningsFromClient:
    oracle_earnings_client_singleton_instance = EarningsClientRepository

    @staticmethod
    def get_account_by_region(portfolios: dict, region: str) -> str:

        accounts_by_region = {
            Region.BR.value: "bmf_account",
            Region.US.value: "dw_account",
        }
        fields = accounts_by_region[region]

        accounts = portfolios.get(fields)
        return accounts

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
    def payable_earnings_data_response(
        cls, earnings_client: EarningsClientModel, accounts: str, open_earnings
    ):

        query_payable_values = open_earnings.build_query_payable_earnings(
            cod_client=accounts,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
            earnings_types=earnings_client.earnings_types,
        )

        payable_earnings_request = (
            open_earnings.oracle_earnings_client_singleton_instance.get_data(
                sql=query_payable_values
            )
        )

        earnings_payable_values = [
            EarningsFromClient.normalize_earnings_data(earnings_res)
            for earnings_res in payable_earnings_request
        ]
        return earnings_payable_values

    @classmethod
    def record_date_earnings_response(
        cls, earnings_client: EarningsClientModel, accounts: str, open_earnings
    ):

        query_record_date_values = open_earnings.build_query_record_date_earnings(
            cod_client=accounts,
            limit=earnings_client.limit,
            offset=earnings_client.offset,
            earnings_types=earnings_client.earnings_types,
        )

        record_date_earnings_request = (
            open_earnings.oracle_earnings_client_singleton_instance.get_data(
                sql=query_record_date_values
            )
        )

        earnings_record_date_values = [
            EarningsFromClient.normalize_earnings_data(earnings_response)
            for earnings_response in record_date_earnings_request
        ]
        return earnings_record_date_values

    @classmethod
    def get_service_response(
        cls, earnings_client: EarningsClientModel, jwt_data: dict
    ) -> dict:

        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})

        region = earnings_client.region.value
        region_portfolios = portfolios.get(region.lower(), {})

        accounts = cls.get_account_by_region(region_portfolios, region)

        region = earnings_client.region.value
        open_earnings = earnings_client_region.get(region)

        earnings_payable_values = []
        earnings_record_date_values = []
        if open_earnings:
            # query result of FUTURE VALUES CONFIRMED earnings (with the date informed)
            earnings_payable_values = EarningsFromClient.payable_earnings_data_response(
                open_earnings=open_earnings,
                earnings_client=earnings_client,
                accounts=accounts,
            )

            # query result of NOT YET CONFIRMED earnings (31-12-9999)
            earnings_record_date_values = EarningsFromClient.record_date_earnings_response(
                open_earnings=open_earnings,
                earnings_client=earnings_client,
                accounts=accounts,
            )

        response = {
            "payable_earnings": earnings_payable_values,
            "record_date_earnings": earnings_record_date_values,
        }

        return response
