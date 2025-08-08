from pydantic_settings import BaseSettings, SettingsConfigDict


class MaxSizeSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VALIDATION__MAX_SIZE_BYTE__")

    ORGANIZATION_LOGO: int
    SUBJECT_LOGO: int
    INDICATOR_EXL: int
