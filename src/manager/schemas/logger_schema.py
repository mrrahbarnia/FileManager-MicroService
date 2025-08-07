from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggerSchema(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOGGING__")
    GENERAL_FORMAT: str

    FORMAT_JSON_NAME: str
    FORMAT_JSON: str
    FORMAT_JSON_PACKAGE: str
    FORMAT_JSON_DATETIME: str

    FORMAT_CONSOLE_NAME: str
    FORMAT_CONSOLE: str
    FORMAT_CONSOLE_DATETIME: str

    HANDLER_CONSOLE_NAME: str
    HANDLER_CONSOLE_FORMATTER: str
    HANDLER_CONSOLE_CLASS: str
    HANDLER_CONSOLE_LEVEL: str

    HANDLER_FILE_NAME: str
    HANDLER_FILE_FORMATTER: str
    HANDLER_FILE_CLASS: str
    HANDLER_FILE_LEVEL: str
    HANDLER_FILE_MAX_BYTES_PER_FILE: int
    HANDLER_FILE_BACKUP_COUNT: int
    HANDLER_FILE_FILENAME: str
