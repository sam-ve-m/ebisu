from src.infrastructures.env_config import config
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class EarningsClientRepository(OracleBaseRepository):
    service = config("ORACLE_SERVICE_EARNINGS_CLIENT")
    user = config("ORACLE_USER_EARNINGS_CLIENT")
    password = config("ORACLE_PASSWORD_EARNINGS_CLIENT")
    base_dns = config("ORACLE_BASE_DNS_EARNINGS_CLIENT")
    port = config("ORACLE_PORT_EARNINGS_CLIENT")
