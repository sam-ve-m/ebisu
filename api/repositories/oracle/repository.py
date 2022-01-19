
class OracleRepository:

    def __init__(self, oracle_connection):
        self.oracle_connection = oracle_connection

    def execute(self, sql):
        connection = self.oracle_connection.acquire()
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
        self.oracle_connection.release(connection)

    def get_one_data(self, sql: str):
        connection = self.oracle_connection.acquire()
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            cursor.rowfactory = lambda *args: dict(zip(columns, args))
            row = cursor.fetchone()
        self.oracle_connection.release(connection)
        return row

    def get_data(self, sql: str):
        connection = self.oracle_connection.acquire()
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            cursor.rowfactory = lambda *args: dict(zip(columns, args))
            rows = cursor.fetchall()
        self.oracle_connection.release(connection)
        return rows
