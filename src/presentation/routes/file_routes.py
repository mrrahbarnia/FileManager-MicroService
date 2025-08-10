from typing import Annotated
import logging

from fastapi import APIRouter, UploadFile, status, Depends, Form, File, Query
from fastapi.responses import StreamingResponse

from src.common.http_response import AppResponse
from src.common import http_exception as exc
from src.common import types
from src.common.pagination import PaginationResponseSchema
from src.presentation.dependencies import get_postgres_repo
from src.presentation.dtos import file_dtos as dtos
from src.infrastructure.repositories.postgres_repo import PostgresRepository
from src.infrastructure.s3 import file_stream_generator_from_s3
from src.service import FileService as Service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AppResponse[dtos.FileRead],
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "status_code": 200,
                        "message": "File created successfully.",
                        "data": {},
                    }
                }
            }
        },
        409: {
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "status_code": 409,
                        "message": "Duplicate entity.",
                        "data": {"name": "Duplicate file name."},
                    }
                }
            }
        },
        413: {
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "status_code": 413,
                        "message": "Max file size exceeded.",
                        "data": {"file_size": "Maximumm size is 1000"},
                    }
                }
            }
        },
        415: {
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "status_code": 415,
                        "message": "Not supported file extensions.",
                        "data": {"file_extension": "File extension must be in []"},
                    }
                }
            }
        },
        500: {
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "status_code": 500,
                        "message": "Unexpected Error.",
                        "data": {},
                    }
                }
            }
        },
    },
)
async def create_file(
    file: Annotated[UploadFile, File()],
    type: Annotated[types.FileTypeEnum, Form()],
    name: Annotated[str, Form(max_length=250)],
    repository: Annotated[PostgresRepository, Depends(get_postgres_repo)],
) -> AppResponse[dtos.FileRead]:
    result = await Service(repository).create_file(name=name, file=file, type=type)
    return AppResponse[dtos.FileRead](
        success=True,
        status_code=status.HTTP_201_CREATED,
        message="File created successfully.",
        data=result,
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=AppResponse[PaginationResponseSchema[list[dtos.FileRead]]],
    responses={
        500: {
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "status_code": 500,
                        "message": "Unexpected Error.",
                        "data": {},
                    }
                }
            }
        },
    },
)
async def list_files(
    filter_query: Annotated[dtos.FileFilterQuery, Query()],
    repository: Annotated[PostgresRepository, Depends(get_postgres_repo)],
) -> AppResponse[PaginationResponseSchema[list[dtos.FileRead]]]:
    result = await Service(repository).list_files(filter_query)
    return AppResponse[PaginationResponseSchema[list[dtos.FileRead]]](
        success=True,
        status_code=status.HTTP_200_OK,
        message="Files fetched successfully.",
        data=result,
    )


@router.delete(
    "/{file_id}",
    status_code=status.HTTP_200_OK,
    response_model=AppResponse[None],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "status_code": 200,
                        "message": "File deleted successfully.",
                        "data": None,
                    }
                }
            }
        },
        404: {
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "status_code": 404,
                        "message": "Entity not found.",
                        "data": {"file_id": "There is no file with the provided ID."},
                    }
                }
            }
        },
        500: {
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "status_code": 500,
                        "message": "Unexpected Error.",
                        "data": {},
                    }
                }
            }
        },
    },
)
async def delete_file(
    file_id: types.FileId,
    repository: Annotated[PostgresRepository, Depends(get_postgres_repo)],
) -> AppResponse[None]:
    await Service(repository).delete_file(file_id)
    return AppResponse[None](
        success=True,
        status_code=status.HTTP_200_OK,
        message="File deleted successfully.",
        data=None,
    )


@router.get("/{file_uuid}", status_code=status.HTTP_200_OK)
async def stream_file(
    file_uuid: str,
    repository: Annotated[PostgresRepository, Depends(get_postgres_repo)],
):
    await Service(repository).stream_file(file_uuid)
    return StreamingResponse(
        file_stream_generator_from_s3(file_uuid),  # type: ignore
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_uuid}"},
    )
