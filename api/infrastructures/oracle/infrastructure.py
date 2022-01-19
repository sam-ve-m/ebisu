import cx_Oracle

from api.core.interfaces.infrastructures.oracle.interface import IInfrastructure


class OracleInfrastructure(IInfrastructure):
    @staticmethod
    def get_connection(service, user, password, base_dns, port):
        return cx_Oracle.SessionPool(
            user=user,
            password=password,
            dsn=cx_Oracle.makedsn(base_dns, port, service_name=service),
        )

