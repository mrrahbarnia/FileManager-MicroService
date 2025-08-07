from functools import lru_cache

from src.infrastructure.repositories.postgres_repo import PostgresRepository
from src.infrastructure.db.meta_data import SESSION_MAKER


@lru_cache
def get_postgres_repo() -> PostgresRepository:
    return PostgresRepository(SESSION_MAKER)
