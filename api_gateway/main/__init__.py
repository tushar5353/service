import os
import sys
import logging
import json

from uuid import uuid4
import time
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from asgi_correlation_id import CorrelationIdMiddleware
from starlette.concurrency import iterate_in_threadpool

from service.api_gateway.main.settings import get_settings
from service.api_gateway.routers.service_router import \
    service_router
from service.utils.logs import configure_logging
from service.utils import database

SETTINGS = get_settings()

def create_app():
    """
    * Loads Config
    * Creatd FastAPI's object
    * Includes all the endpoints
    * Add Middlewares
    * Returns FastAPI's instance (app)

    :return: `FastAPI()`
    """

    logging.info("STARTING APP!!")
    service = os.environ["SERVICE"]
    # Creating FastAPI app
    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        try:
            configure_logging()
            logger.info("startup")
            database.make_migrations()
        except Exception as e:
            logging.info(e, exc_info=True)

    logger = logging.getLogger(os.environ["RUN_TYPE"])
    # Middleware for adding uuid for each request in logs
    app.add_middleware(
        CorrelationIdMiddleware,
        header_name='X-Request-ID',
        generator=lambda: uuid4().hex,
        transformer=lambda a: a[:16],
    )

    async def log_request_info(request: Request):
        request_body = await request.json()
    
        logger.info(
            f"{request.method} request to {request.url} metadata->"
            f"\tHeaders: {request.headers}"
            f"\tBody: {request_body}"
            f"\tPath Params: {request.path_params}"
            f"\tQuery Params: {request.query_params}"
            f"\tCookies: {request.cookies}"
        )

    if service=="service":
        app.include_router(service_router, dependencies=[Depends(log_request_info)])

    # Middleware for handline CORS,allowed methods, allowed headers etc.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=SETTINGS.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        try:
            start_time = time.time()
            response = await call_next(request)
            response.headers["X-Process-Time"] = str(time.time() - start_time)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            logger.info(f"response_body={response_body[0].decode()[:1000]} {response.headers}")
            return response
        except Exception as e:
            logger.error(f"Error:: {e}", exc_info=True)

    return app
