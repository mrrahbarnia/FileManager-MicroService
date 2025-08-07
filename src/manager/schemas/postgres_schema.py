from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQLSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRESQL__")

    HOST: str
    PORT: str
    DATABASE: str
    USERNAME: str
    PASSWORD: str
    DRIVER: str
    MINIMUM_NUMBER_OF_CONNECTION: int
    MAXIMUM_NUMBER_OF_CONNECTION: int
    MAXIMUM_QUERIES_TO_RESTART_CONNECTION: int
    MAXIMUM_INACTIVE_CONNECTION_LIFETIME_IN_SECOND: int
    TIMEOUT_PER_QUERY: float
