import os
from uuid import uuid4

from typing import Annotated, TypedDict, BinaryIO
from fastapi import UploadFile, HTTPException
from pydantic import AfterValidator

from src.common.http_exception import FileMustHaveNameException


def strip_str(s: str) -> str:
    return s.strip()


StrippedStr = Annotated[str, AfterValidator(strip_str)]


class ImageDict(TypedDict):
    image: UploadFile
    allowable_extensions: list[str]
    max_size: int
    extensions_exc: HTTPException
    max_size_exc: HTTPException


def validate_images_and_return_unique_names(
    images: list[ImageDict],
) -> list[tuple[str, BinaryIO]]:
    image_unique_names: list[tuple[str, BinaryIO]] = []
    for index, image in enumerate(images):
        if image["image"].filename:
            image_ext = os.path.splitext(image["image"].filename)[1]
            unique_name_with_ext = f"{uuid4()}{image_ext}"
            image_unique_names.append((f"{unique_name_with_ext}", image["image"].file))
        else:
            raise FileMustHaveNameException(
                data={"image": f"File number {index} must have name."}
            )
    return image_unique_names
