from src.infrastructures.env_config import config
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class EarningsClientRepository(OracleBaseRepository):
    service = config("ORACLE_BASE_SERVICE_BR")
    user = config("ORACLE_BASE_USER")
    password = config("ORACLE_BASE_PASSWORD")
    base_dns = config("ORACLE_BASE_DSN")
    port = config("ORACLE_BASE_PORT")
