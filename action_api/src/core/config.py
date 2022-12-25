from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class ApiSettings(BaseSettings):
    project_name: str = 'UGC'
    kafka_host: str = 'localhost'
    kafka_port: int = 9092
    access_token_secret_key: str = '256-bit-secret-key-1'
    token_algoritm: str = 'HS256'


api_settings = ApiSettings()
