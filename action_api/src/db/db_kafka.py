from aiokafka import AIOKafkaProducer

NAME_TOPIC_FRAME = 'movies-frames'

db_producer: AIOKafkaProducer | None = None


async def get_kafka() -> AIOKafkaProducer:
    return db_producer
