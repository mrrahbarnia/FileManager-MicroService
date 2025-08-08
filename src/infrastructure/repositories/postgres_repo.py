from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.common import types, http_exception as exc
from src.infrastructure.db import db_models
from src.presentation.dtos import file_dtos as dtos


class PostgresRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session = session_maker

    async def get_all_files_with_counter(
        self, filter_qeury: dtos.FileFilterQuery
    ) -> tuple[Sequence[tuple[db_models.File]], int]:
        conditions = []
        if filter_qeury.name__exact:
            conditions.append(db_models.File.name == filter_qeury.name__exact)
        if filter_qeury.name__icontain:
            conditions.append(
                db_models.File.name.ilike(f"%{filter_qeury.name__icontain}%")
            )

        limit, offset = filter_qeury.to_limit_offset()
        stmt = sa.select(db_models.File).where(*conditions).limit(limit).offset(offset)
        counter_stmt = sa.select(sa.func.count(stmt.c.id))
        async with self._session.begin() as session:
            result = (await session.execute(stmt)).tuples().all()
            counter_result = await session.scalar(counter_stmt)
            if counter_result is None:
                raise exc.DBError
        return result, counter_result

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
