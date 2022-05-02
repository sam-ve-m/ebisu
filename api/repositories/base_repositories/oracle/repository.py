from etria_logger import Gladsheim

from api.infrastructures.connections.oracle.infrastructure import OracleInfrastructure


class OracleBaseRepository:

    infra = OracleInfrastructure
    oracle_connection = None
    service = None
    user = None
    password = None
    base_dns = None
    port = None

    @classmethod
    def _get_connection(cls):
        if cls.oracle_connection is None:
            cls.oracle_connection = cls.infra.get_connection(
                service=cls.service,
                user=cls.user,
                password=cls.password,
                base_dns=cls.base_dns,
                port=cls.port,
            )
        return cls.oracle_connection

    @classmethod
    def execute(cls, sql):
        oracle_connection = cls._get_connection()
        connection = oracle_connection.acquire()
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
        oracle_connection.release(connection)

    @classmethod
    def get_one_data(cls, sql: str):
        oracle_connection = cls._get_connection()
        connection = oracle_connection.acquire()
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            cursor.rowfactory = lambda *args: dict(zip(columns, args))
            row = cursor.fetchone()
        oracle_connection.release(connection)
        return row

    @classmethod
    def get_data(cls, sql: str):
        try:
            oracle_connection = cls._get_connection()
            connection = oracle_connection.acquire()
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                cursor.rowfactory = lambda *args: dict(zip(columns, args))
                rows = cursor.fetchall()
            oracle_connection.release(connection)
            return rows
        except Exception as ex:
            Gladsheim.error(error=ex, msg="Error when get date in oracle database")
