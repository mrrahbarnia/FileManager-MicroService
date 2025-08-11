from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.manager import ENVS


def setup_middlewares(app: FastAPI) -> None:
    setup_cors(app)


def setup_cors(app: FastAPI):
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++ setup cors")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ENVS.CORS.ALLOW_ORIGINS,
        allow_credentials=ENVS.CORS.ALLOW_CREDENTIALS,
        allow_methods=ENVS.CORS.ALLOW_METHODS,
        allow_headers=ENVS.CORS.ALLOW_HEADERS,
    )
