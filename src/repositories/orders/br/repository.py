from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class BrOrdersRepository(OracleBaseRepository):
    @classmethod
    def _get_connection(cls):
        return cls.infra.get_base_connection_br()
