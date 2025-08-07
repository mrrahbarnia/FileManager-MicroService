from pydantic import BaseModel

from src.manager import ENVS


class LogConfig(BaseModel):
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict[str, dict[str, str]] = {
        ENVS.LOGGING.FORMAT_CONSOLE_NAME: {
            "format": ENVS.LOGGING.FORMAT_CONSOLE,
            "datefmt": ENVS.LOGGING.FORMAT_CONSOLE_DATETIME,
        },
        ENVS.LOGGING.FORMAT_JSON_NAME: {
            "()": ENVS.LOGGING.FORMAT_JSON_PACKAGE,
            "fmt": ENVS.LOGGING.FORMAT_JSON,
            "datefmt": ENVS.LOGGING.FORMAT_JSON_DATETIME,
        },
    }
    handlers: dict[str, dict[str, str | int]] = {
        ENVS.LOGGING.HANDLER_CONSOLE_NAME: {
            "class": ENVS.LOGGING.HANDLER_CONSOLE_CLASS,
            "level": ENVS.LOGGING.HANDLER_CONSOLE_LEVEL,
            "formatter": ENVS.LOGGING.HANDLER_CONSOLE_FORMATTER,
        },
        ENVS.LOGGING.HANDLER_FILE_NAME: {
            "class": ENVS.LOGGING.HANDLER_FILE_CLASS,
            "level": ENVS.LOGGING.HANDLER_FILE_LEVEL,
            "formatter": ENVS.LOGGING.HANDLER_FILE_FORMATTER,
            "filename": ENVS.LOGGING.HANDLER_FILE_FILENAME,
            "maxBytes": ENVS.LOGGING.HANDLER_FILE_MAX_BYTES_PER_FILE,
            "encoding": "utf-8",
            "backupCount": ENVS.LOGGING.HANDLER_FILE_BACKUP_COUNT,
        },
    }
