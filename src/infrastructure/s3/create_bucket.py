import logging

from aiobotocore.session import get_session # type: ignore
from botocore.config import Config # type: ignore

from src.manager import ENVS

logger = logging.getLogger(__name__)


async def create_bucket(bucket_name: str) -> None:
    session = get_session()
    async with session.create_client(
        "s3",
        endpoint_url=ENVS.S3.URL,
        aws_access_key_id=ENVS.S3.ROOT_USER,
        aws_secret_access_key=ENVS.S3.ROOT_PASSWORD,
        region_name=ENVS.S3.REGION_NAME,
        config=Config(s3={"addressing_style": "path"}),
    ) as client:
        try:
            await client.create_bucket(Bucket=ENVS.S3.BUCKET_NAME)  # type: ignore
        except Exception:
            logger.info(f"Bucket {bucket_name} already exist.")
