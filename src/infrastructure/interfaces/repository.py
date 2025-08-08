from typing import Protocol, Sequence

from src.common import types
from src.infrastructure.db import db_models
from src.presentation.dtos import file_dtos as dtos


class RepositoryInterface(Protocol):
    async def get_all_files_with_counter(
        self, filter_qeury: dtos.FileFilterQuery
    ) -> tuple[Sequence[tuple[db_models.File]], int]: ...

    async def create_file(
        self,
        name: str,
        file_name: str,
        type: types.FileTypeEnum,
        size: int,
        extension: str,
    ) -> types.FileId | None: ...

    async def get_file_by_name(self, name: str) -> tuple[db_models.File] | None: ...
