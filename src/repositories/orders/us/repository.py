from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class UsOrdersRepository(OracleBaseRepository):
    @classmethod
    def _get_connection(cls):
        return cls.infra.get_base_connection_us()
