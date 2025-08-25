import logging
import sys
import os
import time
from contextvars import ContextVar

from asgi_correlation_id import correlation_id
from fastapi import APIRouter, Depends, HTTPException, Body

from service.api_gateway.routers import schemas
from service.utils.kafka_utils.producer import AIOProducer
from service.utils import config

# Initialize the logger
logger = logging.getLogger(os.environ["RUN_TYPE"])

config_obj = config.Config()
env_config = config_obj.get_config("environment")

service_router = APIRouter(prefix="/service",
                             tags=["service"],)

aio_producer = AIOProducer()
cnt = 0

def ack(err, msg):
    global cnt
    cnt = cnt + 1

@service_router.post("/test_timeout")
async def test_timeout(request: schemas.TestTimeout):
    try:
        time.sleep(request.test_value)
        return {"status":"success"}
    except Exception as e:
        logger.error(f"Error::{e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@service_router.post("/add_user")
async def add_user(request: schemas.AddUser):
    try:
        users.add(request.user_name, request.email)
        return {"status":"success"}
    except Exception as e:
        logger.error(f"Error::{e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@service_router.post("/order")
async def add_user(request: schemas.NewOrder):
    try:
        api_producer.produce("test-topic",
                             {"user_id": request.user_id,
                              "product": request.product,
                              "quantity": request.quantity})
        return {"status":"success"}
    except Exception as e:
        logger.error(f"Error::{e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
