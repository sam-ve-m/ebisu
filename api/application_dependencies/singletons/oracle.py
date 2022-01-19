from api.infrastructures.oracle.infrastructure import OracleInfrastructure
from api.repositories.oracle.repository import OracleRepository
from api.utils.env_config import config


class OracleSingletonInstance:

    oracle_us_singleton_instance = None
    oracle_br_singleton_instance = None

    @classmethod
    def get_oracle_us_singleton_instance(cls):
        if cls.oracle_us_singleton_instance is None:
            infra = OracleInfrastructure.get_connection(service=config('ORACLE_SERVICE_US'))
            cls.oracle_us_singleton_instance = OracleRepository(infra)

        return cls.oracle_us_singleton_instance

    @classmethod
    def get_oracle_br_singleton_instance(cls):
        if cls.oracle_br_singleton_instance is None:
            infra = OracleInfrastructure.get_connection(service=config('ORACLE_SERVICE_BR'))
            cls.oracle_br_singleton_instance = OracleRepository(infra)

        return cls.oracle_br_singleton_instance

