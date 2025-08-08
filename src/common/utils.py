import os
from uuid import uuid4

from typing import Annotated, BinaryIO
from fastapi import UploadFile
from pydantic import AfterValidator

from src.manager import ENVS
from src.common import types, http_exception as exc


def strip_str(s: str) -> str:
    return s.strip()


StrippedStr = Annotated[str, AfterValidator(strip_str)]


UniqueFileNameWithExt = str
FileBinary = BinaryIO
FileSize = int
FileExtension = str


def validate_images_and_return_meta_data(
    file: UploadFile,
    type: types.FileTypeEnum,
) -> tuple[UniqueFileNameWithExt, FileBinary, FileSize, FileExtension]:
    file_ext = os.path.splitext(file.filename)[1]  # type: ignore
    for file_type, file_max_size in ENVS.MAX_SIZE_VALIDATION:
        if file_type == type:
            if file.size > file_max_size:
                raise exc.MaxFileSizeExceedException(
                    data={"file_size": f"Maximumm size is {file_max_size}"}
                )
    for (
        file_type,
        file_allowable_extenstions,
    ) in ENVS.ALLOWABLE_EXTENSTION_VALIDATION:
        if file_type == type:
            if file_ext not in file_allowable_extenstions:
                raise exc.NotAllowedFileExtensionsException(
                    data={
                        "file_extension": f"File extension must be in {file_allowable_extenstions}"
                    }
                )
    unique_name_with_ext = f"{uuid4()}{file_ext}"
    assert file.size
    return unique_name_with_ext, file.file, file.size, file_ext
