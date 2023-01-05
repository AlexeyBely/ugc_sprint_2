from motor.motor_asyncio import AsyncIOMotorClient


client: AsyncIOMotorClient | None = None


async def get_modgodb() -> AsyncIOMotorClient:
    return client
