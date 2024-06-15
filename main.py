import logging
from contextlib import asynccontextmanager
from http import HTTPStatus
from logging.config import dictConfig

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

import api
from core.config.app import settings
from core.di import init_di
from core.errors import ApplicationError
from core.logger.config import StructureLogConfig
from core.middlewares.http_request import HTTPRequestMiddleware

logger = logging.getLogger(__name__)


def init_cors(app: FastAPI) -> None:
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["Content-Type"],
        )


def init_routers(app: FastAPI) -> None:
    app.include_router(api.router_v1)


def init_listeners(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={
                "error_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                "message": HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            },
        )

    @app.exception_handler(ApplicationError)
    async def app_exception_handler(request: Request, exc: ApplicationError):
        content = exc.to_dict()
        logger.exception(content)
        return JSONResponse(
            status_code=exc.status_code,
            content=content,
        )


def init_middleware(app: FastAPI) -> None:
    app.add_middleware(HTTPRequestMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup event
    dictConfig(StructureLogConfig().model_dump())
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("uvicorn.error").disabled = True
    logger.info("Application startup complete.")
    yield
    # shutdown event


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    init_cors(app=app)
    init_routers(app=app)
    init_listeners(app=app)
    init_middleware(app=app)
    init_di()
    return app


app = create_app()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(str(app.docs_url))


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck():
    response = dict(error=False, msg="success")
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)
