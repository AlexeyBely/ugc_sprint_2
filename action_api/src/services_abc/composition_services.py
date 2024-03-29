from functools import lru_cache
from fastapi import Depends

from db.db_mongo import get_modgodb, MotorClient
from services.likes import MongoLikesService
from services.reviews import MongoReviewsService
from services.bookmarks import MongoBookmarksService


@lru_cache()
def get_likes_service(
    client: MotorClient = Depends(get_modgodb)
) -> MongoLikesService:
    """interface and movie service connectivity."""
    return MongoLikesService(client)


@lru_cache()
def get_reviews_service(
    client: MotorClient = Depends(get_modgodb),
) -> MongoReviewsService:
    """interface and movie service connectivity."""
    return MongoReviewsService(client)


@lru_cache()
def get_bookmarks_service(
    client: MotorClient = Depends(get_modgodb),
) -> MongoBookmarksService:
    """interface and movie service connectivity."""
    return MongoBookmarksService(client)
