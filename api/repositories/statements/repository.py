from api.infrastructures.env_config import config
from api.repositories.base_repositories.oracle.repository import OracleBaseRepository


class StatementsRepository(OracleBaseRepository):
    service = config('ORACLE_SERVICE_STATEMENT')
    user = config("ORACLE_USER_STATEMENT")
    password = config("ORACLE_PASSWORD_STATEMENT")
    base_dns = config("ORACLE_BASE_DSN_STATEMENT")
    port = config("ORACLE_PORT_STATEMENT")