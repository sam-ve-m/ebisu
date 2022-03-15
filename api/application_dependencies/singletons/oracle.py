from api.infrastructures.oracle.infrastructure import OracleInfrastructure
from api.repositories.oracle.repository import OracleRepository
from api.utils.env_config import config
from etria_logger import Gladsheim


class OracleSingletonInstance:
    oracle_us_singleton_instance = None
    oracle_br_singleton_instance = None
    statement_singleton_instance = None
    earnings_singleton_instance = None

    @classmethod
    def get_oracle_us_singleton_instance(cls):
        if cls.oracle_us_singleton_instance is None:
            try:
                infra = OracleInfrastructure.get_connection(service=config('ORACLE_SERVICE_US'),
                                                            user=config("ORACLE_USER_ORDERS"),
                                                            password=config("ORACLE_PASSWORD_ORDERS"),
                                                            base_dns=config("ORACLE_BASE_DSN_ORDERS"),
                                                            port=config("ORACLE_PORT_ORDERS")
                                                            )
                cls.oracle_us_singleton_instance = OracleRepository(infra)
            except Exception as exception:
                Gladsheim.error(
                    message=f"""OracleSingletonInstance::get_oracle_us_singleton_instance::Error on infra connection
                    service={config('ORACLE_SERVICE_US')},
                    user={config("ORACLE_USER_ORDERS")},
                    password={config("ORACLE_PASSWORD_ORDERS")},
                    base_dns={config("ORACLE_BASE_DSN_ORDERS")},
                    port={config("ORACLE_PORT_ORDERS")}:
                    {exception}""",
                    error=exception
                )

        return cls.oracle_us_singleton_instance

    @classmethod
    def get_oracle_br_singleton_instance(cls):
        if cls.oracle_br_singleton_instance is None:
            try:
                infra = OracleInfrastructure.get_connection(service=config('ORACLE_SERVICE_BR'),
                                                            user=config("ORACLE_USER_ORDERS"),
                                                            password=config("ORACLE_PASSWORD_ORDERS"),
                                                            base_dns=config("ORACLE_BASE_DSN_ORDERS"),
                                                            port=config("ORACLE_PORT_ORDERS")
                                                            )

                cls.oracle_br_singleton_instance = OracleRepository(infra)
            except Exception as exception:
                Gladsheim.error(
                    message=f"""OracleInfrastructure::get_oracle_br_singleton_instance::Error on infra connection
                    service={config('ORACLE_SERVICE_BR')},
                    user={config("ORACLE_USER_ORDERS")},
                    password={config("ORACLE_PASSWORD_ORDERS")},
                    base_dns={config("ORACLE_BASE_DSN_ORDERS")},
                    port={config("ORACLE_PORT_ORDERS")}:
                    {exception}""",
                    error=exception
                )

        return cls.oracle_br_singleton_instance

    @classmethod
    def get_statement_singleton_instance(cls):
        if cls.statement_singleton_instance is None:
            try:
                infra = OracleInfrastructure.get_connection(service=config('ORACLE_SERVICE_STATEMENT'),
                                                            user=config("ORACLE_USER_STATEMENT"),
                                                            password=config("ORACLE_PASSWORD_STATEMENT"),
                                                            base_dns=config("ORACLE_BASE_DSN_STATEMENT"),
                                                            port=config("ORACLE_PORT_STATEMENT")
                                                            )

                cls.statement_singleton_instance = OracleRepository(infra)
            except Exception as exception:
                Gladsheim.error(
                    message=f"""OracleInfrastructure::get_statement_singleton_instance::Error on infra connection
                    service={config('ORACLE_SERVICE_STATEMENT')},
                    user={config("ORACLE_USER_STATEMENT")},
                    password={config("ORACLE_PASSWORD_STATEMENT")},
                    base_dns={config("ORACLE_BASE_DSN_STATEMENT")},
                    port={config("ORACLE_PORT_STATEMENT")}:
                    {exception}""",
                    error=exception
                )

        return cls.statement_singleton_instance

    @classmethod
    def get_earnings_singleton_instance(cls):
        if cls.earnings_singleton_instance is None:
            try:
                infra = OracleInfrastructure.get_connection(service=config('ORACLE_SERVICE_EARNINGS'),
                                                            user=config("ORACLE_USER_EARNINGS"),
                                                            password=config("ORACLE_PASSWORD_EARNINGS"),
                                                            base_dns=config("ORACLE_BASE_DNS_EARNINGS"),
                                                            port=config("ORACLE_PORT_EARNINGS")
                                                            )
                cls.earnings_singleton_instance = OracleRepository(infra)
            except Exception as exception:
                Gladsheim.error(
                    message=f"""OracleInfrastructure::get_earnings_singleton_instance::Error on infra connection
                    service = {config('ORACLE_SERVICE_EARNINGS')},
                    user = {config("ORACLE_USER_EARNINGS")},
                    password = {config("ORACLE_PASSWORD_EARNINGS")},
                    base_dns = {config("ORACLE_BASE_DNS_EARNINGS")},
                    port = {config("ORACLE_PORT_EARNINGS")}:
                    {exception}""",
                    error=exception
                )

        return cls.earnings_singleton_instance
