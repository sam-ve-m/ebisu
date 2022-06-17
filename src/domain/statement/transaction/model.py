from src.domain.statement.region_date_format.enum import RegionDateFormat


class Transaction:

    def __init__(self, transaction: dict, region_date_format: RegionDateFormat):
        self.__date = transaction.get("DT_LANCAMENTO")
        self.__description = transaction.get("DS_LANCAMENTO")
        self.__value = transaction.get("VL_LANCAMENTO")
        self.__region_date_format = region_date_format


    def get_formatted_transaction(self):
        formatted_transaction = {

        }