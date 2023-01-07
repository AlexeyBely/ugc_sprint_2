from motor.motor_asyncio import AsyncIOMotorClient
from core.config import api_settings as setting


class MotorClient:
    """stub for library motor.motor_asyncio."""

    def __init__(self, url: str):
        self.url = url
        self.client_mongodb = AsyncIOMotorClient(
            self.url, 
            uuidRepresentation='pythonLegacy'
        )


client: MotorClient


async def get_modgodb() -> MotorClient:
    return client
