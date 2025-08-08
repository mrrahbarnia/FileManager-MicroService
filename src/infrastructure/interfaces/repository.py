from typing import Protocol

from src.common import types
from src.infrastructure.db import db_models


class RepositoryInterface(Protocol):
    async def create_file(
        self,
        name: str,
        file_name: str,
        type: types.FileTypeEnum,
        size: int,
        extension: str,
    ) -> types.FileId | None: ...

    async def get_file_by_name(self, name: str) -> tuple[db_models.File] | None: ...
