from typing import Annotated

from fastapi import APIRouter, UploadFile, status, Depends, Form, File, Query

from src.common.http_response import AppResponse
from src.common import types
from src.common.pagination import PaginationResponseSchema
from src.presentation.dependencies import get_postgres_repo
from src.presentation.dtos import file_dtos as dtos
from src.infrastructure.repositories.postgres_repo import PostgresRepository
from src.service import FileService as Service

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
        404: {
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
