
from decouple import config

from api.infrastructures.oracle.infrastructure import OracleInfrastructure


class OracleRepository(OracleInfrastructure):

    @classmethod
    def instance(cls):
        oracle_connection = cls.get_connection(
            user=config("ORACLE_USER"),
            password=config("ORACLE_PASSWORD"),
            dsn=config("ORACLE_BASE_DSN"),
            port=config("ORACLE_PORT"),
            service=config("ORACLE_SERVICE"),

        )
        return cls(oracle_connection=oracle_connection)

    def __init__(self, oracle_connection):
        self.oracle_connection = oracle_connection

    def execute(self, sql):
        with self.oracle_connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()

    def get_one_data(self, sql: str):
        with self.oracle_connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                cursor.rowfactory = lambda *args: dict(zip(columns, args))
                row = cursor.fetcone()

        return row

    def get_data(self, sql: str):
        with self.oracle_connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                cursor.rowfactory = lambda *args: dict(zip(columns, args))
                rows = cursor.fetchall()

        return rows