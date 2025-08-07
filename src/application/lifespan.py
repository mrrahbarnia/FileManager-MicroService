import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from logging.config import dictConfig

from fastapi import FastAPI

from src.manager import ENVS
from src.application.logger import LogConfig
from src.infrastructure.s3 import create_bucket

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # ============================== On startup
    logger.info("Logger is running...")
    dictConfig(LogConfig().model_dump())

    logger.info("Creating S3 bucket...")
    try:
        await create_bucket(ENVS.S3.BUCKET_NAME)
    except Exception as ex:
        logger.critical(ex)

    logger.info("Application is running...")
    yield

    # ============================== On shutdown
