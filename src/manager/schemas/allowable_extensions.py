from pydantic_settings import BaseSettings, SettingsConfigDict


class AllowableExtenstionSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VALIDATION__ALLOWABLE_EXTENSIONS__")

    ORGANIZATION_LOGO: list[str]
    SUBJECT_LOGO: list[str]
    INDICATOR_EXL: list[str]
