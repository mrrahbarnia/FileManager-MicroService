from fastapi import APIRouter

from src.manager import ENVS
from src.presentation.routes import router

router_v1 = APIRouter(prefix=f"/{ENVS.GENERAL.MICROSERVICE_NAME}/v1")

# ================ Including application routers here ================ #

router_v1.include_router(
    router, prefix=ENVS.ENDPOINT.PREFIX_FILES, tags=ENVS.ENDPOINT.TAGS_FILES
)
