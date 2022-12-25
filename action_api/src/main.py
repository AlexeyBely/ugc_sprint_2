import uvicorn

from api.v1 import frame
from core.config import api_settings
from db import db_kafka

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from aiokafka import AIOKafkaProducer


app = FastAPI(
    title=f'Сервис {api_settings.project_name}',
    docs_url='/ugc/api/openapi',
    openapi_url='/ugc/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Сервис загрузки в kafka',
    version='1.0.1',
)


@app.on_event('startup')
async def startup():
    db_kafka.db_producer = AIOKafkaProducer(
        bootstrap_servers=f'{api_settings.kafka_host}:{api_settings.kafka_port}'
    )
    await db_kafka.db_producer.start()


@app.on_event('shutdown')
async def shutdown():
    await db_kafka.db_producer.stop()


app.include_router(frame.router, prefix='/ugc/api/v1/frame', tags=['frame'])
