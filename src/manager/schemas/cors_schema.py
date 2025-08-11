from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CORS__")

    # Endpoint prefixes
    ALLOW_ORIGINS: list[str]
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: list[str]
    ALLOW_HEADERS: list[str]
