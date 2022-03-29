import cx_Oracle

from api.core.interfaces.infrastructures.oracle.interface import IInfrastructure
from etria_logger import Gladsheim


class OracleInfrastructure(IInfrastructure):

    @staticmethod
    def get_connection(service, user, password, base_dns, port):
        oracle_connection = cx_Oracle.SessionPool(
            user=user,
            password=password,
            dsn=cx_Oracle.makedsn(base_dns, port, service_name=service),
        )
        if oracle_connection is None:
            try:
                return oracle_connection
            except Exception as exception:
                Gladsheim.error(
                    message=
                    f"OracleInfrastructure::get_connection:: Error on getting the oracle connection, {exception}",
                    error=exception,
                )
        return oracle_connection
