import cx_Oracle

from api.core.interfaces.infrastructures.oracle.interface import IInfrastructure

x_dsn = """(DESCRIPTION=
(FAILOVER=ON)
(LOAD_BALANCE=ON)
(ADDRESS=(PROTOCOL=TCP)(HOST=172.20.16.244)(PORT=1521))
(ADDRESS=(PROTOCOL=TCP)(HOST=172.20.16.249)(PORT=1521))
(ADDRESS=(PROTOCOL=TCP)(HOST=172.20.17.52)(PORT=1521))
(CONNECT_DATA=
(SERVER=DEDICATED)
(SERVICE_NAME=OPDBHYPE.subdbexaclipriv.vcndb.oraclevcn.com)
(FAILOVER_MODE=
(TYPE=select)
(METHOD=basic))))"""


class OracleInfrastructure(IInfrastructure):
    @staticmethod
    def get_connection(user, password, dsn, port, service):
        return cx_Oracle.connect(
            user=user,
            password=password,
            dsn=x_dsn

        )

    @classmethod
    def get_singleton_connection(cls, **kwargs):
        pass
