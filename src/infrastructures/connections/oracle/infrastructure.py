import cx_Oracle

from src.core.interfaces.infrastructures.oracle.interface import IOracleInfrastructure
from src.infrastructures.env_config import config
from etria_logger import Gladsheim


class OracleInfrastructure(IOracleInfrastructure):

    _base_connection_br = None
    _base_connection_us = None
    _position_connection = None

    @classmethod
    def get_base_connection_br(cls):
        dsn = config("ORACLE_BASE_CONNECTION_STRING_BR")
        if cls._base_connection_br is None:
            cls._base_connection_br = cls._get_connection(dsn)
        return cls._base_connection_br

    @classmethod
    def get_base_connection_us(cls):
        dsn = config("ORACLE_BASE_CONNECTION_STRING_US")
        if cls._base_connection_us is None:
            cls._base_connection_us = cls._get_connection(dsn)
        return cls._base_connection_us

    @classmethod
    def get_position_connection(cls):
        dsn = config("ORACLE_POSITION_CONNECTION_STRING")
        if cls._position_connection is None:
            cls._position_connection = cls._get_connection(dsn)
        return cls._position_connection

    @staticmethod
    def _get_connection(dsn):
        try:
            connection = cx_Oracle.SessionPool(
                user=config("ORACLE_BASE_CONNECTION_USER"),
                password=config("ORACLE_BASE_CONNECTION_PASS"),
                dsn=dsn,
            )
            return connection
        except Exception as exception:
            Gladsheim.error(
                message=f"OracleInfrastructure::get_connection:: Error on getting the oracle connection, {exception}",
                error=exception,
            )
            raise exception


if __name__ == "__main__":
    OracleInfrastructure.get_position_connection()
