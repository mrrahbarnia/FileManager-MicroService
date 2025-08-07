from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy import types as sql_types
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    create_async_engine,
)

from src.manager import ENVS

POSTGRES_DSN = f"{ENVS.GENERAL.CURRENT_DB}+{ENVS.POSTGRESQL.DRIVER}://{ENVS.POSTGRESQL.USERNAME}:{ENVS.POSTGRESQL.PASSWORD}@{ENVS.POSTGRESQL.HOST}:{ENVS.POSTGRESQL.PORT}/{ENVS.POSTGRESQL.DATABASE}"

ASYNC_ENGINE: AsyncEngine = create_async_engine(POSTGRES_DSN)
SESSION_MAKER = async_sessionmaker(ASYNC_ENGINE, expire_on_commit=False)


class BaseModel(DeclarativeBase, MappedAsDataclass):
    type_annotation_map = {
        datetime: sql_types.TIMESTAMP(timezone=True),
        # CHAR(26) for storing ULID.
    }
