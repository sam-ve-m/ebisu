from api.infrastructures.env_config import config
from api.repositories.base_repositories.oracle.repository import OracleBaseRepository


class EarningsRepository(OracleBaseRepository):
    service = config('ORACLE_SERVICE_EARNINGS')
    user = config("ORACLE_USER_EARNINGS")
    password = config("ORACLE_PASSWORD_EARNINGS")
    base_dns = config("ORACLE_BASE_DNS_EARNINGS")
    port = config("ORACLE_PORT_EARNINGS")