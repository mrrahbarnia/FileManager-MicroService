import os
from uuid import uuid4

from typing import Annotated, BinaryIO
from fastapi import UploadFile, HTTPException
from pydantic import AfterValidator


def strip_str(s: str) -> str:
    return s.strip()


StrippedStr = Annotated[str, AfterValidator(strip_str)]


UniqueFileNameWithExt = str
FileBinary = BinaryIO
FileSize = int
FileExtension = str


def validate_images_and_return_meta_data(
    file: UploadFile,
    allowable_extensions: list[str],
    max_size: int,
    extensions_exc: HTTPException,
    max_size_exc: HTTPException,
) -> tuple[UniqueFileNameWithExt, FileBinary, FileSize, FileExtension]:
    file_ext = os.path.splitext(file.filename)[1]  # type: ignore
    if file_ext not in allowable_extensions:
        raise extensions_exc
    unique_name_with_ext = f"{uuid4()}{file_ext}"
    if file_size := file.size:
        if file_size > max_size:
            raise max_size_exc
    assert file_size is not None
    return unique_name_with_ext, file.file, file_size, file_ext
