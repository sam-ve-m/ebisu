from api.core.interfaces.infrastructures.oracle.interface import IOracle
from api.infrastructures.oracle.infrastructure import OracleInfrastructure
from api.utils.env_config import config


class OracleRepository(IOracle):

    def __init__(self):
        self.infra = self.get_infrastructure()

    def get_infrastructure(self):
        infra = OracleInfrastructure()
        return infra.get_connection(
            user=config("ORACLE_USER"),
            password=config("ORACLE_PASSWORD"),
            dsn=config("ORACLE_BASE_DSN"),
            port=config("ORACLE_PORT"),
            service=config("ORACLE_SERVICE"),
        )

    def execute(self, sql: str):
        with self.infra as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()

    def get_one_data(self, sql: str):
        with self.infra as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                cursor.rowfactory = lambda *args: dict(zip(columns, args))
                row = cursor.fetcone()

        return row

    def get_data(self, sql: str):
        with self.infra as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                cursor.rowfactory = lambda *args: dict(zip(columns, args))
                rows = cursor.fetchall()

        return rows