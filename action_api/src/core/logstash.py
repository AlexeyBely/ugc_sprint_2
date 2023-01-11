import logging
from logstash_async.handler import AsynchronousLogstashHandler, LogstashFormatter

from core.config import api_settings as setting


logger = logging.getLogger('')


def config_logstash():
    formatter = LogstashFormatter(tags=['action_app', ])
    handler = AsynchronousLogstashHandler(
        setting.logstash_host, 
        setting.logstash_port,
        transport='logstash_async.transport.UdpTransport',
        database_path='logstash.db',
    )
    handler.formatter = formatter
    logger.addHandler(handler)


def add_log_request_id(request_id: str | None):
    logger.info(f'request_id {request_id}')
