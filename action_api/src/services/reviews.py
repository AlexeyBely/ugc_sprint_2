import uuid

from datetime import datetime
from db.db_mongo import MotorClient
from bson import ObjectId

from services_abc.reviews_abc import BaseReviewsService
from core.config import api_settings as setting
from services.utils import UtilsService


class MongoReviewsService(BaseReviewsService, UtilsService):
    """read/write docs to reviews collection."""

    def __init__(self, client: MotorClient):
        self.client = client.client_mongodb
        self.db = self.client[setting.mongodb_db]
        self.collection = self.db[setting.mongodb_coll_reviews]

    async def id_details(self, review_id: str) -> dict:
        """Load details review doc."""
        id = ObjectId(review_id)
        review = await self.collection.find_one({'_id': id})
        return review

    async def read_reviews(
        self,
        user_id: uuid.UUID,
        movie_id: uuid.UUID | None = None,
        size: int = 1,
        page: int = 20,
    ) -> dict:
        """
        Load review from user_id or movie_id.
        
        If movie_id equal None, then read reviews by user_id. Or
        movie_id not equal None, then read reviews by movie_id
        """
        if movie_id is not None:
            find = {'movie_id': movie_id}
        else:
            find = {'user_id': user_id}
        pages = await self.read_to_paginate(size, page, find)
        return pages

    async def add_review(self, user_id: uuid.UUID, movie_id: uuid.UUID, 
                         text: str) -> dict:
        """Add new review."""
        review = await self.collection.find_one({'user_id': user_id, 
                                                 'movie_id': movie_id})
        if review is None:
            new_review = {
                'user_id': user_id,
                'movie_id': movie_id,
                'review': text,
                'like': await self.read_like_reiting(user_id, movie_id),
                'created': datetime.now(),
                'modified': datetime.now(),
            }
            review_obj = await self.collection.insert_one(new_review)
            review_id = review_obj.inserted_id
        else:
            update = {
                'review': text,
                'like': await self.read_like_reiting(user_id, movie_id),
                'modified': datetime.now(),
            }
            review_obj = await self.collection.update_one(
                {'_id': review['_id']}, {'$set': update}
            )
            review_id = review['_id']
        new_review = await self.collection.find_one({'_id': review_id})
        return new_review

    async def delete_review(
        self, user_id: uuid.UUID, movie_id: uuid.UUID
    ) -> dict | None:
        """delete the review."""
        return await self.delete_doc(user_id, movie_id)
