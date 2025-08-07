from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class PostgresRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session = session_maker
