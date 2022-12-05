from abc import ABC, abstractmethod
from etria_logger import Gladsheim

from src.infrastructures.connections.oracle.infrastructure import OracleInfrastructure


class OracleBaseRepository(ABC):

    infra = OracleInfrastructure

    @abstractmethod
    def _get_connection():
        ...

    @classmethod
    def execute(cls, sql):
        oracle_connection = cls._get_connection()
        connection = oracle_connection.acquire()
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
        oracle_connection.release(connection)

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
            Gladsheim.error(
                error=ex, msg="Error when get date in oracle database", sql=sql
            )
            raise ex

    @classmethod
    def fetch_one(cls, sql: str):
        try:
            oracle_connection = cls._get_connection()
            connection = oracle_connection.acquire()
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                cursor.rowfactory = lambda *args: dict(zip(columns, args))
                rows = cursor.fetchone()
            oracle_connection.release(connection)
            return rows
        except Exception as ex:
            Gladsheim.error(
                error=ex, msg="Error when fetch_one in oracle database", sql=sql
            )
            raise ex
