from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Schema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="S3__")

    URL: str
    HOST_NAME: str
    ROOT_USER: str
    CONNECTION_PROTOCOL: Literal["http", "https"]
    ROOT_PASSWORD: str
    API_PORT_NUMBER: int
    REGION_NAME: str
    CONSOLE_PORT_NUMBER: int
    BUCKET_NAME: str
