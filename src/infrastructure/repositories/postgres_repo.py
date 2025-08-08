import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.common import types
from src.infrastructure.db import db_models


class PostgresRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session = session_maker

    async def create_file(
        self,
        name: str,
        file_name: str,
        type: types.FileTypeEnum,
        size: int,
        extension: str,
    ) -> types.FileId | None:
        stmt = (
            sa.insert(db_models.File)
            .values(
                {
                    db_models.File.name: name,
                    db_models.File.extension: extension,
                    db_models.File.size: size,
                    db_models.File.type: type,
                    db_models.File.file_name: file_name,
                }
            )
            .returning(db_models.File.id)
        )
        async with self._session.begin() as session:
            return await session.scalar(stmt)

    async def get_file_by_name(self, name: str) -> tuple[db_models.File] | None:
        stmt = sa.select(db_models.File).where(db_models.File.name == name).limit(1)

        async with self._session.begin() as session:
            return (await session.execute(stmt)).tuples().first()
