import cx_Oracle

from api.core.interfaces.infrastructures.oracle.interface import IInfrastructure


class OracleInfrastructure(IInfrastructure):
    @staticmethod
    def get_connection(user, password, dsn, port, service):
        return cx_Oracle.connect(
            user=user,
            password=password,
            dsn=cx_Oracle.makedsn(dsn, port, service_name=service),
        )

    @classmethod
    def get_singleton_connection(cls, **kwargs):
        pass
