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
        return cls._get_connection(dsn, cls._base_connection_br)

    @classmethod
    def get_base_connection_us(cls):
        dsn = config("ORACLE_BASE_CONNECTION_STRING_US")
        return cls._get_connection(dsn, cls._base_connection_us)

    @classmethod
    def get_position_connection(cls):
        dsn = config("ORACLE_POSITION_CONNECTION_STRING")
        return cls._get_connection(dsn, cls._position_connection)

    @staticmethod
    def _get_connection(dsn, connection):
        try:
            if connection is None:
                connection = cx_Oracle.SessionPool(dsn)
            return connection
        except Exception as exception:
            Gladsheim.error(
                message=f"OracleInfrastructure::get_connection:: Error on getting the oracle connection, {exception}",
                error=exception,
            )
            raise exception
