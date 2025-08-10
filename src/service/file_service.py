import logging

from fastapi import UploadFile

from src.common import types, http_exception as exc
from src.common.utils import validate_images_and_return_meta_data
from src.common.pagination import PaginationResponseSchema, PaginationResponse
from src.infrastructure.interfaces.repository import RepositoryInterface
from src.infrastructure.s3 import (
    upload_to_s3,
    delete_from_s3,
)
from src.presentation.dtos import file_dtos as dtos

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self, repository: RepositoryInterface) -> None:
        self._repository = repository

    async def stream_file(self, file_uuid: str):
        try:
            file = await self._repository.get_file_by_uuid(file_uuid)
            if not file:
                raise exc.EntityNotFoundException(data={"file_uuid": "File not found."})

        except exc.EntityNotFoundException as ex:
            logger.info(ex)
            raise

        except Exception as ex:
            logger.critical(ex)
            raise exc.UnexpectedError(data=str(ex))

    async def delete_file(self, file_id: types.FileId) -> None:
        try:
            deleted_file_info = await self._repository.delete_file(file_id)
            if deleted_file_info is None:
                raise exc.EntityNotFoundException(
                    data={"file_id": "There is no file with the provided ID."}
                )
            _, deleted_file_name = deleted_file_info
            await delete_from_s3(deleted_file_name)

        except exc.EntityNotFoundException as ex:
            logger.info(ex)
            raise

        except Exception as ex:
            logger.critical(ex)
            raise exc.UnexpectedError(data=str(ex))

    async def list_files(
        self, filter_qeury: dtos.FileFilterQuery
    ) -> PaginationResponseSchema[list[dtos.FileRead]]:
        try:
            files, count = await self._repository.get_all_files_with_counter(
                filter_qeury
            )
            return PaginationResponseSchema(
                pagination=PaginationResponse(
                    current_page=filter_qeury.page_number,
                    page_size=filter_qeury.page_size,
                    total=count,
                ),
                data=[
                    dtos.FileRead(
                        id=file[0].id,
                        url=file[0].file_name,
                        name=file[0].name,
                        size=file[0].size,
                        extension=file[0].extension,
                        type=file[0].type,  # type: ignore
                    )
                    for file in files
                ],
            )
        except Exception as ex:
            logger.critical(ex)
            raise exc.UnexpectedError(data=str(ex))

    async def create_file(self, name: str, type: types.FileTypeEnum, file: UploadFile):
        try:
            generated_file_name, file_binary, file_size, file_ext = (
                validate_images_and_return_meta_data(file=file, type=type)
            )

            is_name_exist = await self._repository.get_file_by_name(name=name)
            if is_name_exist:
                raise exc.DuplicateEntityException(
                    data={"name": "Duplicate file name."}
                )

            await upload_to_s3(file=file_binary, unique_filename=generated_file_name)
            file_id = await self._repository.create_file(
                file_name=generated_file_name,
                name=name,
                type=type,
                size=file_size,
                extension=file_ext,
            )
            if not file_id:
                raise exc.DBError

            return dtos.FileRead(
                id=file_id,
                url=generated_file_name,
                name=name,
                size=file_size,
                extension=file_ext,
                type=type,
            )

        except (
            exc.DuplicateEntityException,
            exc.NotAllowedFileExtensionsException,
            exc.MaxFileSizeExceedException,
        ) as ex:
            logger.info(ex)
            raise

        except Exception as ex:
            logger.critical(ex)
            raise exc.UnexpectedError(data=str(ex))
