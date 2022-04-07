from api.infrastructures.env_config import config
from api.repositories.base_repositories.oracle.repository import OracleBaseRepository


class UsOrdersRepository(OracleBaseRepository):
    service = config("ORACLE_SERVICE_US")
    user = config("ORACLE_USER_ORDERS")
    password = config("ORACLE_PASSWORD_ORDERS")
    base_dns = config("ORACLE_BASE_DSN_ORDERS")
    port = config("ORACLE_PORT_ORDERS")
