from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GENERAL__")

    APPLICATION_NAME: str
    MICROSERVICE_NAME: str
    CURRENT_DB: str
    PYTHONIC_APPLICATION_NAME: str
    APPLICATION_DESCRIPTION: str
    APPLICATION_VERSION: str
