import cx_Oracle

from src.core.interfaces.infrastructures.oracle.interface import IOracleInfrastructure
from etria_logger import Gladsheim


class OracleInfrastructure(IOracleInfrastructure):
    @staticmethod
    def get_connection(service, user, password, base_dns, port):
        try:
            oracle_connection = cx_Oracle.SessionPool(
                user=user,
                password=password,
                dsn=cx_Oracle.makedsn(base_dns, port, service_name=service),
            )
            return oracle_connection
        except Exception as exception:
            Gladsheim.error(
                message=f"OracleInfrastructure::get_connection:: Error on getting the oracle connection, {exception}",
                error=exception,
            )
            raise exception
