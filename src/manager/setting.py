from enum import StrEnum, auto
from functools import lru_cache

from pydantic import BaseModel

from src.manager import schemas


class ENVIRONMENT(StrEnum):
    PRODUCTION = auto()
    DEVELOPMENT = auto()


class _ENVS(BaseModel):
    RUN_MODE: ENVIRONMENT = ENVIRONMENT.DEVELOPMENT

    LOGGING: schemas.LoggerSchema = schemas.LoggerSchema()  # type: ignore
    FASTAPI: schemas.FastAPISchema = schemas.FastAPISchema()  # type: ignore
    UVICORN: schemas.UvicornSchema = schemas.UvicornSchema()  # type: ignore
    GENERAL: schemas.GeneralSchema = schemas.GeneralSchema()  # type: ignore
    POSTGRESQL: schemas.PostgreSQLSchema = schemas.PostgreSQLSchema()  # type: ignore
    S3: schemas.S3Schema = schemas.S3Schema()  # type: ignore
    VALIDATION: schemas.ValidationSchema = schemas.ValidationSchema()  # type: ignore


@lru_cache
def get_envs() -> _ENVS:
    return _ENVS()  # type: ignore


ENVS = get_envs()
