from pydantic_settings import BaseSettings, SettingsConfigDict


class ValidationSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VALIDATION__")

