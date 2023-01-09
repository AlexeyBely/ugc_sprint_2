from api.v1 import likes, reviews, bookmarks
from core.config import api_settings as setting
from core.logstash import config_logstash, add_log_request_id
from db import db_mongo

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
import sentry_sdk


sentry_sdk.init(
    setting.dns_sentry,
    traces_sample_rate=1.0,
)


app = FastAPI(
    title=f'Сервис {setting.project_name}',
    docs_url='/action/api/openapi',
    openapi_url='/action/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Сервис загрузки/чтения действий пользователей',
    version='1.0.1',
)


@app.middleware("http")
async def log_middle(request: Request, call_next):
    """Middleware to append request_id to logs."""
    if 'X-Request-Id' in request.headers:
        request_id = request.headers['X-Request-Id']
    else:
        request_id = None   
    add_log_request_id(request_id)
    response = await call_next(request)
    return response


@app.on_event('startup')
async def startup():
    db_mongo.client = db_mongo.MotorClient(setting.mongodb_url)
    config_logstash()        


app.include_router(likes.router, prefix='/action/api/v1/likes', tags=['likes'])
app.include_router(reviews.router, prefix='/action/api/v1/reviews', tags=['reviews'])
app.include_router(bookmarks.router, prefix='/action/api/v1/bookmarks', 
                   tags=['bookmarks'])


@app.get(
    "/action/api/sentry-debug",
    summary='Тест отправки исключений',
    description='Проверка что неотловленные исключения доставляются в Sentry',
)
async def trigger_error():
    division_by_zero = 1 / 0

