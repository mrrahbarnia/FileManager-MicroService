from typing import Any

from fastapi import HTTPException, status

from src.manager import ENVS, ENVIRONMENT


class AppBaseException(HTTPException):
    def __init__(
        self,
        *,
        message: str,
        success: bool,
        status_code: int,
        data: Any | None = None,
    ):
        if isinstance(data, Exception):
            if ENVS.RUN_MODE == ENVIRONMENT.PRODUCTION:
                self.data = None
            else:
                self.data = str(data)
        else:
            self.data = data

        self.message = message
        self.status_code = status_code
        self.success = success
        super().__init__(status_code=status_code)


class UnexpectedError(AppBaseException):
    def __init__(self, data: str, message: str = "Unexpected Error."):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            data=data,
        )


class S3StorageException(AppBaseException):
    def __init__(self, data: str, message: str = "S3 storage error."):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            data=data,
        )


class DBError(AppBaseException):
    def __init__(self, data: dict = {}, message: str = "DB error."):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            data=data,
        )


class EntityNotFoundException(AppBaseException):
    def __init__(self, data: dict, message: str = "Entity not found."):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            success=False,
            data=data,
        )


class DuplicateEntityException(AppBaseException):
    def __init__(self, data: dict, message: str = "Duplicate entity."):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            success=False,
            data=data,
        )


class FileError(AppBaseException):
    def __init__(self, data: str, message: str = "Something wrong with file metadata."):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
            data=data,
        )


class NotAllowedFileExtensionsException(AppBaseException):
    def __init__(self, data: dict, message: str = "Not supported file extensions."):
        super().__init__(
            message=message,
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            success=False,
            data=data,
        )


class MaxFileSizeExceedException(AppBaseException):
    def __init__(self, data: dict, message: str = "Max file size exceeded."):
        super().__init__(
            message=message,
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            success=False,
            data=data,
        )
