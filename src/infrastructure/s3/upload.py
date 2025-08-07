import logging
from typing import BinaryIO

from aiobotocore.session import get_session  # type: ignore
from botocore.config import Config  # type: ignore

from src.manager import ENVS
from src.infrastructure.exceptions import S3Error

logger = logging.getLogger(__name__)


async def upload_to_s3(file: BinaryIO, unique_filename: str) -> None:
    try:
        session = get_session()
        async with session.create_client(
            "s3",
            endpoint_url=ENVS.S3.URL,
            aws_access_key_id=ENVS.S3.ROOT_USER,
            aws_secret_access_key=ENVS.S3.ROOT_PASSWORD,
            region_name=ENVS.S3.REGION_NAME,
            config=Config(s3={"addressing_style": "path"}),
        ) as client:
            await client.put_object(
                Bucket=ENVS.S3.BUCKET_NAME, Key=unique_filename, Body=file
            )  # type: ignore
    except Exception as ex:
        logger.critical("Uploading to S3 bucket failed.", exc_info=ex)
        raise S3Error(ex) from ex
