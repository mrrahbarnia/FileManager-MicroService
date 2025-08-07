import logging

from src.common import types
from src.common import http_exception as exc
from src.common.pagination import PaginationResponseSchema, PaginationResponse
from src.infrastructure.interfaces.repository import RepositoryInterface
from src.presentation.dtos import file_dtos as dtos

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self, repository: RepositoryInterface) -> None:
        self._repository = repository