from pydantic import BaseModel, field_serializer

from src.manager import ENVS
from src.common import types


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
