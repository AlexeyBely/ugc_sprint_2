import uvicorn

from api.v1 import likes, reviews, bookmarks
from core.config import api_settings as setting
from db import db_mongo

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient


app = FastAPI(
    title=f'Сервис {setting.project_name}',
    docs_url='/action/api/openapi',
    openapi_url='/action/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Сервис загрузки/чтения действий пользователей',
    version='1.0.1',
)


@app.on_event('startup')
async def startup():
    db_mongo.client = AsyncIOMotorClient(
        setting.mongodb_url, uuidRepresentation='pythonLegacy',
    )


@app.on_event('shutdown')
async def shutdown():
    pass


app.include_router(likes.router, prefix='/action/api/v1/likes', tags=['likes'])
app.include_router(reviews.router, prefix='/action/api/v1/reviews', tags=['reviews'])
app.include_router(bookmarks.router, prefix='/action/api/v1/bookmarks', 
                   tags=['bookmarks'])

