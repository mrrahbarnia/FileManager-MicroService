from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="UVICORN_SERVER__")

    APP: str
    HOST: str
    PORT: int
    LOG_LEVEL: str
    PROXY_HEADERS: bool
    FORWARDED_ALLOW_IPS: str
    RELOAD: bool
    LOOP: Literal["none", "auto", "asyncio", "uvloop"]
    WORKERS: int
    SERVER_HEADER: bool
