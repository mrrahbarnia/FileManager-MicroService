from uvicorn import run as run

from src.manager.setting import ENVS


if __name__ == "__main__":
    run(
        app=ENVS.UVICORN.APP,
        host=ENVS.UVICORN.HOST,
        port=ENVS.UVICORN.PORT,
        log_level=ENVS.UVICORN.LOG_LEVEL.lower(),
        proxy_headers=ENVS.UVICORN.PROXY_HEADERS,
        forwarded_allow_ips=ENVS.UVICORN.FORWARDED_ALLOW_IPS,
        reload=ENVS.UVICORN.RELOAD,
        loop=ENVS.UVICORN.LOOP,
        workers=ENVS.UVICORN.WORKERS,
        server_header=ENVS.UVICORN.SERVER_HEADER,
    )
