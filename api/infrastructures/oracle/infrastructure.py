import cx_Oracle


class OracleInfrastructure:

    @staticmethod
    def get_connection(user, password, dsn, port, service):
        return cx_Oracle.connect(
            user=user,
            password=password,
            dsn=cx_Oracle.makedsn(
                dsn,
                port,
                service_name=service)

        )