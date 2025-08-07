from fastapi import APIRouter

from src.manager import ENVS
# from src.presentation.routes import v1

router_v1 = APIRouter(prefix=f"/{ENVS.GENERAL.MICROSERVICE_NAME}/v1")

# ================ Including application routers here ================ #

# router_v1.include_router(
#     v1.tag_router, prefix=ENVS.ENDPOINT.PREFIX_TAGS, tags=ENVS.ENDPOINT.TAGS_TAGS
# )
