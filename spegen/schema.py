from __future__ import annotations
from typing import Dict, Any
from pydantic import BaseModel, validator

from data import ENV_PARAMETERS


class EnvVector(BaseModel):
    __root__: Dict[str, Any]

    @validator('__root__')
    def check_params(cls, v):
        for key, val in v.items():
            if key not in ENV_PARAMETERS:
                raise ValueError(f"Unknown parameter {key}")
        return v
