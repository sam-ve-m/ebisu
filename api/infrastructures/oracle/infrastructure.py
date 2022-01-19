import cx_Oracle

from api.core.interfaces.infrastructures.oracle.interface import IInfrastructure
from api.utils.env_config import config


class OracleInfrastructure(IInfrastructure):
    @staticmethod
    def get_connection(service):
        return cx_Oracle.SessionPool(
            user=config("ORACLE_USER"),
            password=config("ORACLE_PASSWORD"),
            dsn=cx_Oracle.makedsn(config("ORACLE_BASE_DSN"), config("ORACLE_PORT"), service_name=service),
        )

