# STANDARD LIBS
from __future__ import annotations
from pydantic import BaseModel, validator

from src.domain.validators.user_account.brazil_register_number_validator import is_cpf_valid


class Cpf(BaseModel):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, e):
        if is_cpf_valid(cpf=e):
            return e.replace(".", "").replace("-", "").replace("/", "")
        raise ValueError("invalid cpf")
