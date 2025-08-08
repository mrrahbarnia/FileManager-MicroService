from typing import Annotated

from pydantic import BaseModel, Field, field_serializer

from src.manager import ENVS
from src.common import types
from src.common.pagination import PaginationSchema
from src.common.utils import StrippedStr


class FileBase(BaseModel):
    id: types.FileId
    url: str
    name: str
    size: int
    extension: str

    @field_serializer("url", mode="plain")
    def serialize_logo(self, value: str | None) -> str | None:
        if value:
            return f"{ENVS.S3.URL}/{ENVS.S3.BUCKET_NAME}/{value}"
        return value


class FileRead(FileBase): ...


class FileFilterQuery(PaginationSchema):
    name__icontain: Annotated[
        StrippedStr | None,
        Field(
            description="File name must contain this query parameter (case-insensitive)."
        ),
    ] = None
    name__exact: Annotated[
        StrippedStr | None,
        Field(
            description="File name must be exactly this query parameter (case-sensitive)."
        ),
    ] = None
