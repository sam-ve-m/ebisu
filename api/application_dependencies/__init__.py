from typing import Tuple
from fastapi import Depends

from api.application_dependencies.jwt_validator import verify_jwt_token


GLOBAL_APPLICATION_DEPENDENCIES: Tuple[Depends] = (
    Depends(verify_jwt_token),
)

API_TITLE = "Customer Exchange Information"
API_DESCRIPTION = "Dados de clientes"
