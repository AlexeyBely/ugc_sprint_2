from aiokafka import AIOKafkaProducer

from models.response_models import Response
from services_base.base_movie import BaseMovieService
from db.db_kafka import NAME_TOPIC_FRAME


class KafkaMovieService(BaseMovieService):
    """Load to kafka."""

    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def add_frame_movie(
        self, user_id: str, movie_id: str, frame: int
    ) -> Response | None:
        """Save frame movie."""
        key = f'{user_id}+{movie_id}'.encode('UTF-8')
        value = str(frame).encode('UTF-8')
        try:
            await self.producer.send_and_wait(
                topic=NAME_TOPIC_FRAME, value=value, key=key,
            )
        except Exception as e:
            return {'result': f'{type(e)}: {e}'}
        finally:
            return {'result': 'recording was successful'}
