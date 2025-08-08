from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class EndpointSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ENDPOINT__")

    # Endpoint prefixes
    PREFIX_FILES: str

    # Endpoint tags
    TAGS_FILES: list[str | Enum] | None
