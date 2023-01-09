from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field


logging_config.dictConfig(LOGGING)


class ApiSettings(BaseSettings):
    project_name: str = 'Actions users'
    mongodb_url = 'mongodb://0.0.0.0:27019, 0.0.0.0:27020'
    mongodb_db: str = 'actionsDb'
    mongodb_coll_likes: str = 'likes'
    mongodb_coll_reviews: str = 'reviews'
    mongodb_coll_bookmarks: str = 'bookmarks'
    access_token_secret_key: str = '256-bit-secret-key-1'
    token_algoritm: str = 'HS256'
    default_page_size: int = 20
    max_page_size: int = 100
    dns_sentry: str = 'https://examplePublicKey@o0.ingest.sentry.io/0'
    logstash_host = '127.0.0.1'
    logstash_port = 5044


api_settings = ApiSettings()
