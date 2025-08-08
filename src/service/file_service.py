import logging

from fastapi import UploadFile

from src.manager import ENVS
from src.common import types, http_exception as exc
from src.common.utils import validate_images_and_return_meta_data
from src.common.pagination import PaginationResponseSchema, PaginationResponse
from src.infrastructure.interfaces.repository import RepositoryInterface
from src.infrastructure.s3 import upload_to_s3
from src.presentation.dtos import file_dtos as dtos

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self, repository: RepositoryInterface) -> None:
        self._repository = repository

    async def create_file(self, name: str, type: types.FileTypeEnum, file: UploadFile):
        try:
            max_size = 0
            allowable_extensions: list[str] = list()
            extensions_exc = None
            max_size_exc = None

            for file_type, file_max_size in ENVS.MAX_SIZE_VALIDATION:
                if file_type == type:
                    max_size = file_max_size
                    max_size_exc = exc.MaxFileSizeExceedException(
                        data={"file_size": f"Maximumm size is {file_max_size}"}
                    )
            for (
                file_type,
                file_allowable_extenstions,
            ) in ENVS.ALLOWABLE_EXTENSTION_VALIDATION:
                if file_type == type:
                    allowable_extensions = file_allowable_extenstions
                    extensions_exc = exc.NotAllowedFileExtensionsException(
                        data={
                            "file_extension": f"File extension must be in {file_allowable_extenstions}"
                        }
                    )
            generated_file_name, file_binary, file_size, file_ext = (
                validate_images_and_return_meta_data(
                    file=file,
                    allowable_extensions=allowable_extensions,
                    max_size=max_size,
                    extensions_exc=extensions_exc,  # type: ignore
                    max_size_exc=max_size_exc,  # type: ignore
                )
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
