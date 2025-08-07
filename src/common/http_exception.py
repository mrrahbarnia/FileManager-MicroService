from typing import Any

from fastapi import HTTPException

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
            status_code=500,
            success=False,
            data=data,
        )


class S3StorageException(AppBaseException):
    def __init__(self, data: str, message: str = "S3 storage error."):
        super().__init__(
            message=message,
            status_code=500,
            success=False,
            data=data,
        )


class DBError(AppBaseException):
    def __init__(self, data: dict = {}, message: str = "DB error."):
        super().__init__(
            message=message,
            status_code=500,
            success=False,
            data=data,
        )


class EntityNotFoundException(AppBaseException):
    def __init__(self, data: dict, message: str = "Entity not found."):
        super().__init__(
            message=message,
            status_code=404,
            success=False,
            data=data,
        )


class DuplicateEntityException(AppBaseException):
    def __init__(self, data: dict, message: str = "Duplicate entity."):
        super().__init__(
            message=message,
            status_code=400,
            success=False,
            data=data,
        )


class FileMustHaveNameException(AppBaseException):
    def __init__(self, data: dict, message: str = "File must have name."):
        super().__init__(
            message=message,
            status_code=400,
            success=False,
            data=data,
        )


class NotAllowedFileExtensionsException(AppBaseException):
    def __init__(self, data: dict, message: str = "Not supported file extensions."):
        super().__init__(
            message=message,
            status_code=415,
            success=False,
            data=data,
        )


class MaxFileSizeExceedException(AppBaseException):
    def __init__(self, data: dict, message: str = "Max file size exceeded."):
        super().__init__(
            message=message,
            status_code=413,
            success=False,
            data=data,
        )
