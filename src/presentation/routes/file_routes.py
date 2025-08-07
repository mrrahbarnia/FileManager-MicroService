from typing import Annotated

from fastapi import APIRouter, status, Depends, Query

from src.common.http_response import AppResponse
from src.common import types
from src.common.pagination import PaginationResponseSchema
from src.presentation.dependencies import get_postgres_repo
from src.presentation.dtos import file_dtos as dtos
from src.infrastructure.repositories.postgres_repo import PostgresRepository
from src.service import file_service as Service

router = APIRouter()

# @router.get()
