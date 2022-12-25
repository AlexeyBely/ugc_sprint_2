from functools import lru_cache
from typing import Type

from db.db_kafka import get_kafka
from services.movie import KafkaMovieService

from fastapi import Depends
from aiokafka import AIOKafkaProducer


@lru_cache()
def get_movie_service(producer: AIOKafkaProducer = Depends(get_kafka)
                      ) -> KafkaMovieService:
    """interface and movie service connectivity."""
    return KafkaMovieService(producer)
