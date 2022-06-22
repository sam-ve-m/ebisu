from src.infrastructures.env_config import config
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class UserPositionsRepository(OracleBaseRepository):
    service = config("ORACLE_POSITION_SERVICE")
    user = config("ORACLE_POSITION_USER")
    password = config("ORACLE_POSITION_PASSWORD")
    base_dns = config("ORACLE_POSITION_DSN")
    port = config("ORACLE_POSITION_PORT")
