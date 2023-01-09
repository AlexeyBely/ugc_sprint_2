import logging
from logging import config as logging_config
from logstash_async.handler import AsynchronousLogstashHandler

from core.config import api_settings as setting


logger = logging.getLogger('')


def config_logstash():
    handler = AsynchronousLogstashHandler(
        setting.logstash_host, 
        setting.logstash_port,
        transport='logstash_async.transport.UdpTransport',
        database_path='logstash.db'
    )
    logger.addHandler(handler)


def add_log_request_id(request_id: str | None):
    logger.info(f'request_id {request_id}')
